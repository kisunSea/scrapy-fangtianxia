# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from .items import NewHouseItem
from .items import SecondHandHouseItem

class FangtianxiaPipeline(object):

    def __init__(self):
        self.newhouse_fp = open('./newhouse_info.json', 'wb')
        self.secondhouse_fp = open('./oldhouse.json', 'wb')
        self.newhouse_export = JsonLinesItemExporter(file=self.newhouse_fp, ensure_ascii=False)
        self.secondhouse_export = JsonLinesItemExporter(file=self.secondhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_export.export_item(item)
        else:
            self.secondhouse_export.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
        self.secondhouse_fp.close()
