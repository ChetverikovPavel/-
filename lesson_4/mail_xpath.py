import re
import requests
from lxml import html
from pymongo import MongoClient
from hashlib import sha256
from pprint import pprint

def mongo_insert(new_list):
    for el in new_list:
        hash_id = sha256(format(el).encode("utf-8")).hexdigest()
        try:
            collection.insert_one({'_id': hash_id} | el)
        except:
            continue


url = 'https://lenta.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//time[@class='g-time']/..")

item_list = []
for item in items:
    items_data = {}

    name = item.xpath('./text()')
    name = str(name[0])
    if '\xa0' in name:
        name = name.replace('\xa0', ' ')

    link = item.xpath('./@href')

    info = item.xpath('./time[@class="g-time"]/@datetime')
    if link[0][0] == 'h':
        item_url = re.search('\w*://\w*[.]\w*', link[0]).group(0)
        items_data['url'] = item_url
    else:
        link[0] = url + link[0]
        items_data['url'] = url

    items_data['name'] = name
    items_data['link'] = link
    items_data['info'] = info

    item_list.append(items_data)

client = MongoClient('127.0.0.1', 27017)
db = client['lenta']
collection = db.news
mongo_insert(item_list)

for el in collection.find({}):
    pprint(el)