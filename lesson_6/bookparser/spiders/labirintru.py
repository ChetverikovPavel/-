import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = [
        'https://www.labirint.ru/search/%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F/?stype=0&page=1']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="cover"]/@href').getall()
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        book_url = response.url
        book_name = response.xpath('//h1/text()').get()
        book_author = response.xpath('//a[@data-event-label="author"]/text()').get()
        book_price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        if not book_price:
            book_price = response.xpath('//span[@class="buying-price-val-number"]/text()').get()

        book_price_sale = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()

        book_rate = response.xpath('//div[@id="rate"]/text()').get()
        book_currency = response.xpath('//span[@class="buying-pricenew-val-currency"]/text()').get()
        yield BookparserItem(url=book_url, name=book_name, author=book_author, price=book_price,
                             price_sale=book_price_sale, rate=book_rate, currency=book_currency)
