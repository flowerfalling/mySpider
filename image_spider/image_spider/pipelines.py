# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return Request(item['image_urls'])

    def item_completed(self, results, item, info):
        print(item['id'])
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['id']}.jpg"
