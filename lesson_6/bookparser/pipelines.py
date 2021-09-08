# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.book0809

    def process_item(self, item, spider):
        if item['author']:
            item['name'] = self.process_name(item['name'])
        item['price'] = int(item['price'])
        try:
            item['price_sale'] = int(item['price_sale'])
        except:
            pass
        item['rate'] = float(item['rate'])
        collections = self.mongo_base[spider.name]
        collections.insert_one(item)
        return item

    def process_name(self, name):
        name = name.split(':')
        name = ':'.join(name[1:])
        return name

