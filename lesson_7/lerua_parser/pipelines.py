# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib as hl
from pymongo import MongoClient


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class LeruaParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua1309

    def process_item(self, item, spider):
        item_dict = {}
        item_list = []
        for el in range(len(item['spec_left'])):
            item_list.append(item['spec_left'][el] + ': ' + item['spec_right'][el])
        item_dict['specifications'] = item_list
        item_dict['url'] = item['url']
        item_dict['name'] = item['name']
        item_dict['photos'] = item['photos']
        item_dict['price info'] = {}
        item_dict['price info']['price'] = item['price']
        item_dict['price info']['curr'] = item['currency']
        item_dict['price info']['unit'] = item['unit']
        item_dict['url'] = item['url']
        item_dict['_id'] = hl.sha256(str(item).encode('utf-8')).hexdigest()
        collections = self.mongo_base[spider.name]
        collections.insert_one(item_dict)
        return item
