# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value


def process_spec_right(value):

    value = value.replace('\n', '').strip()
    return value


class LeruaParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    spec_left = scrapy.Field()
    spec_right = scrapy.Field(input_processor=MapCompose(process_spec_right))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
