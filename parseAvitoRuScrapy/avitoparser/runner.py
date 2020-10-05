from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser import settings
from avitoparser.spiders.avitoru import AvitoruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoruSpider, search='котята')

    process.start()
