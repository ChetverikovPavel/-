import scrapy
from scrapy.http import HtmlResponse
from lerua_parser.items import LeruaParserItem
from scrapy.loader import ItemLoader


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    # /search/?q=%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B&fromRegion=34&page=2
    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={query}&fromRegion=34']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@data-qa-product=""]/a')
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('currency', '//span[@slot="currency"]/text()')
        loader.add_xpath('unit', '//span[@slot="unit"]/text()')
        loader.add_xpath('spec_left', '//dl[@class="def-list"]/div[@class="def-list__group"]/dt/text()')
        loader.add_xpath('spec_right', '//dl[@class="def-list"]/div[@class="def-list__group"]/dd/text()')
        loader.add_xpath('photos', '//picture[@slot="pictures"]/source[contains(@srcset, "2000")]/@srcset')
        loader.add_value('url', response.url)

        yield loader.load_item()
