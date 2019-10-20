"""
该模块主要提供工具类
"""
import threading

Lock = threading.Lock()

class GenCityData(object):
    """提取首页的城市连接"""
    def __new__(cls, *args, **kwargs):
        with Lock:
            if hasattr(cls, '_instance'):
                return cls._instance
            setattr(cls, '_instance', object.__new__(cls))
            return cls._instance

    def __init__(self, res):
        self.res = res

    def _is_valid(self):
        """特别行政区的id与部分省份相同，处理差错"""
        # 排除&nbsp;特殊空格字符
        region_name_list = list(
            filter(lambda x: len(x.get().strip()), self.res.xpath(".//strong/text()"))
        )
        return True if len(region_name_list) == 2 else False

    def _region_format(self):
        if self._is_valid():
            *region_eles, special_region = self.res
            yield region_eles
            yield [special_region,]
        else:
            yield self.res

    def data(self):
        """数据结果集生成器"""
        region_name = None
        for idx, selector_eles in enumerate(self._region_format()):
            if idx == 0:
                region_name = selector_eles[0].xpath('.//strong/text()').get()
                # print(region_name)
            cities = list()
            for selector in selector_eles:
                for city_name, city_link in zip(selector.xpath('.//a/text()'),selector.xpath('.//a/@href')):
                    cities.append((city_name.get(), city_link.get()))
            for ins in cities:
                # print(region_name, ins)

                # 新房地址
                temp1 = ins[-1].split('.')
                temp1.insert(1, 'newhouse')
                newhouse_link_prefix = '.'.join(temp1)
                newhouse_link = newhouse_link_prefix + 'house/s/'

                # 二手房地址
                temp1[1] = 'esf'
                oldhouse_link = '.'.join(temp1)

                # print(region_name, ins[0], newhouse_link, oldhouse_link)
                yield  region_name, ins[0], newhouse_link, oldhouse_link

