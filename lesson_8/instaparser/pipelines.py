# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from hashlib import sha256

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.Insta1609

    def process_item(self, item, spider):
        item['_id'] = sha256(str(item).encode('utf-8')).hexdigest()
        collections = self.mongo_base[spider.name]
        collections.insert_one(item)
        return item
