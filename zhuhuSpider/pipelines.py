# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class zhihuPipeline(object):
    def __init__(self, MONGODB_HOST, MONGODB_PORT):
        self.host = MONGODB_HOST
        self.port = MONGODB_PORT

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            MONGODB_HOST=crawler.settings.get("MONGODB_HOST"),
            MONGODB_PORT=crawler.settings.get("MONGODB_PORT")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client.zhihu
        self.collection = self.db.zhihuuser

    def process_item(self, item, spider):
        self.collection.update({'url_token': item['url_token']}, dict(item), True)
        return item

    def close_spider(self, spider):
        self.client.close()
