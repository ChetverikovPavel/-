# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    price_sale = scrapy.Field()
    rate = scrapy.Field()
    currency = scrapy.Field()
    _id = scrapy.Field()
