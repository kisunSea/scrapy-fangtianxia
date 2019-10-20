# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewHouseItem(scrapy.Item):
    # 小区(楼盘)名
    house_name = scrapy.Field()
    # 居室类型
    house_type = scrapy.Field()
    # 建面
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 更多信息页
    detail_link = scrapy.Field()
    # 售价
    price = scrapy.Field()
    # 联系电话
    mobile = scrapy.Field()
    # 状态
    status = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 地区
    region_name = scrapy.Field()
    # 城市
    city_name = scrapy.Field()


class SecondHandHouseItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 类型
    house_type = scrapy.Field()
    # 建面
    area = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 朝向
    direction = scrapy.Field()
    # 房东
    house_master = scrapy.Field()
    # 地址
    detail_addr = scrapy.Field()
    # 房屋总价值
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 地区
    region_name = scrapy.Field()
    # 城市
    city_name = scrapy.Field()
    # 小区名
    house_name = scrapy.Field()
