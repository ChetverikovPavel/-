from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerua_parser import settings
from lerua_parser.spiders.lerua import LeruaSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = input('Введите запрос для сбора данных:')
    process.crawl(LeruaSpider, query=query)

    process.start()