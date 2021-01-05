# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from creeper.items import coverItem, zlibItem
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

class Search_Pipeline:

    def __init__(self):
        self.file = open('../data/search_results.json', 'wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, zlibItem):
            self.exporter.export_item(item)
        return item

class Getdlink_Pipeline:

    def __init__(self):
        self.file = open('../data/dlink.json', 'wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ZlibImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, coverItem):
            request_objs = super(ZlibImagesPipeline, self).get_media_requests(item, info)
            for requests_obj in request_objs:
                requests_obj.item = item
            return request_objs
    
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    #     return f'full/{image_guid}.jpg'

    def file_path(self, request, response=None, info=None, *,item=None):
        image_name = request.url[-36:]
        return f'{image_name}'