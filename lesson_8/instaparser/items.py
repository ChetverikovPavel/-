# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    parse_user_id = scrapy.Field()
    parse_username = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    picture = scrapy.Field()
    status = scrapy.Field()

