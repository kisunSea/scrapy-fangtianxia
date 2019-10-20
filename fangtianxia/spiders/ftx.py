# -*- coding: utf-8 -*-
import scrapy
from ..utils import GenCityData
import re
from ..items import NewHouseItem
from ..items import SecondHandHouseItem
from urllib import parse

class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fangtianxia.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm',]

    def parse(self, response):
        id_no = 1
        id_prefix = "sffamily_B03_{0}"
        while 1:
            cur_no = id_no if id_no >= 10 else '0' + str(id_no)
            cur_basic_xpath = "//tr[@id='" + id_prefix.format(cur_no) + "']"
            res = response.xpath(cur_basic_xpath)
            if not len(res):
                break
            else:
                g = GenCityData(res)
                for region_name, city_name, newhouse_link, oldhouse_link in g.data():
                    print(region_name, city_name, newhouse_link, oldhouse_link)
                    yield scrapy.Request(
                        url=newhouse_link,
                        callback=self.parse_newhouse,
                        meta={'info': (region_name, city_name)},
                        dont_filter=True,
                    )
                    yield scrapy.Request(
                        url=oldhouse_link,
                        callback=self.parse_oldhouse,
                        meta={'info': (region_name, city_name)},
                        dont_filter=True,
                    )
            id_no += 1

    def parse_newhouse(self, response):
        region_name, city_name = response.meta.get('info')
        house_items = response.xpath("//li//div[contains(@class, 'nlc_details')]")
        for house in house_items:
            format_func = lambda regex, unformate_str, join_tag: re.sub(regex, '', join_tag.join(unformate_str))
            # 小区(楼盘名)
            unformate_name = house.xpath(".//div[contains(@class, 'nlcd_name')]/a/text()").get(),
            house_name = format_func('\s', unformate_name, '')
            # 居室类型
            house_type = list(house.xpath("./div[contains(@class, 'house_type')]/a/text()").getall())
            house_type = '|'.join(house_type)
            # 建面
            unformate_area = house.xpath("./div[contains(@class, 'house_type')]/text()").getall()
            area = format_func('\s|/|－', unformate_area, '')
            # 地址
            unformate_addr = house.xpath(".//div[contains(@class, 'address')]//text()").getall()
            address = format_func('\s', unformate_addr, '')
            # 价格
            unformate_price = house.xpath("./div[@class='nhouse_price']//text()").getall()
            price = format_func('\s|广告', unformate_price, '')
            # 联系电话
            unformate_tel = house.xpath(".//div[@class='tel']/p/text()").getall()
            mobile = unformate_tel[0] if all(unformate_tel) else ""
            # 更多信息页
            detail_link = house.xpath(".//div[contains(@class, 'nlcd_name')]/a/@href").get(),
            detail_link = 'https:'+''.join(list(detail_link))
            # 状态 在售或待售
            status = house.xpath(".//span[@class='inSale']/text()").get()
            # 标签
            tags = house.xpath(".//div[contains(@class,'fangyuan')]/a/text()").getall()
            tags = format_func('\s', tags, '|')

            yield NewHouseItem(
                house_name = house_name,
                house_type = house_type,
                area = area,
                address = address,
                detail_link = detail_link,
                price = price,
                mobile = mobile,
                status = status,
                tags = tags,
                region_name = region_name,
                city_name = city_name
            )

        next_page = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_page:
            yield scrapy.Request(
                url = next_page,
                callback = self.parse_newhouse,
                meta = {'info':(region_name, city_name)},
                dont_filter = True
            )

    def parse_oldhouse(self, response):
        region_name, city_name = response.meta.get('info')
        house_items = response.xpath("//div[contains(@class,'shop_list')]//dl[@id]")
        for house in house_items:
            # 小区名
            house_name = house.xpath(".//p[@class='add_shop']/a/@title").get()
            # 标题
            title = house.xpath("./dd//span[@class='tit_shop']/text()").get()
            detail_list = house.xpath(".//p[contains(@class,'tel_shop')]/text()").getall()
            detail_list = list(map(lambda x: x.strip(), detail_list))
            # 类型、建面、楼层类型、楼层朝向、修建日期
            house_type, area, floor, direction, *_ = detail_list
            # 房东姓名
            house_master = house.xpath(".//span[contains(@class,'people_name')]/a/text()").get()
            # 总价
            total_price = house.xpath("./dd[@class='price_right']/span/b/text()").get()
            # 单价
            unit_price = house.xpath("./dd[@class='price_right']/span//text()").getall()[-1]
            # 地址
            address = house.xpath(".//p[@class='add_shop']/span/text()").get()
            # print(house_name, title, house_type, area, floor, direction, house_master, total_price, unit_price, address)
            yield SecondHandHouseItem(
                title = title,
                house_type = house_type,
                area = area,
                floor = floor,
                direction = direction,
                house_master = house_master,
                detail_addr = address,
                total_price = total_price,
                unit_price = unit_price,
                region_name = region_name,
                city_name = city_name,
                house_name = house_name,
            )

        next = response.xpath("//div[@class='page_al']//p/a[text()='下一页']")
        if bool(next):
            next_url = next.xpath("./@href").extract()[0]
            # print(response.urljoin(next_url))
            yield scrapy.Request(
                url=response.urljoin(next_url),
                callback=self.parse_oldhouse,
                dont_filter=True,
                meta={'info':(region_name, city_name)},
            )




