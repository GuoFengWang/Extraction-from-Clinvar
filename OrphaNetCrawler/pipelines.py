# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class OrphanetcrawlerPipeline(object):
    """结果输出到一个 csv 格式的文件中"""
    def __init__(self):
        self.file = open('OrphaNet_entry.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, fields_to_export=['omim','title','prevalence','onset_age','disease_def','synonym'], encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self, spider):
        pass
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
