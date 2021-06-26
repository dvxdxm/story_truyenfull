# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from itemadapter import ItemAdapter
from bson.json_util import loads, dumps


class ScanstoryPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    collection_name = 'story'

    def __init__(self, mongo_uri, mongo_db):

        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if hasattr(spider, 'collection_name'):
            self.collection_name = spider.collection_name

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        story_name = item["story_name"]
        collection_name = item["collection_name"]
        record = self.db[collection_name].find_one({"story_name": story_name})
        json_str = dumps(record)
        result = loads(json_str)
        # print(f"record _id: {result['_id']}")
        if collection_name == "story":
            if not record:
                self.db[collection_name].insert_one(ItemAdapter(item).asdict())
        elif collection_name == "chapter":
            chapter_title = item["chapter_title"]
            chapter = self.db[collection_name].find_one({"story_name": story_name, "chapter_title": chapter_title})
            if not chapter:
                adapter = ItemAdapter(item)
                if result:
                    adapter['story_id'] = result['_id']

                self.db[collection_name].insert_one(adapter.asdict())
        return item
