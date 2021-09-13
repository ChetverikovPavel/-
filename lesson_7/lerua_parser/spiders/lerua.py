import scrapy
from scrapy.http import HtmlResponse
from lerua_parser.items import LeruaParserItem
from scrapy.loader import ItemLoader

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={query}&fromRegion=34']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@data-qa-product=""]/a')
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

        # name = response.xpath('//h1/text()').get()
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # currency = response.xpath('//span[@slot="currency"]/text()').get()
        # unit = response.xpath('//span[@slot="unit"]/text()').get()
        # url = response.url
        # spec_left = response.xpath('//dl[@class="def-list"]/div[@class="def-list__group"]/dt/text()').getall()
        # spec_right = response.xpath('//dl[@class="def-list"]/div[@class="def-list__group"]/dd/text()').getall()
        # photos = response.xpath('//picture[@slot="pictures"]/source[contains(@srcset, "2000")]/@srcset').getall()
        # yield LeruaParserItem(name=name, price=price, currency=currency, unit=unit, spec_left=spec_left,
        #                       spec_right=spec_right, photos=photos, url=url)

