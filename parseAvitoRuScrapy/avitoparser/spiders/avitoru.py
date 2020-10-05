import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

#https://www.avito.ru/rossiya?q=porsche
class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']

    def __init__(self,search):
        self.start_urls = [f'https://www.avito.ru/rossiya?q={search}']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@class='snippet-link']")
        for link in ads_links:
            yield response.follow(link, callback= self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(),response=response)
        loader.add_xpath('name',"//h1/span/text()")
        loader.add_xpath('price','(//span[@class="js-item-price"])[1]/text()')
        loader.add_xpath('photo',"//div[contains(@class,'gallery-img-wrapper')]/div[contains(@class,'gallery-img-frame')]/@data-url")
        yield loader.load_item()


        # name = response.xpath("//h1/span/text()").extract_first()
        # price = response.xpath('(//span[@class="js-item-price"])[1]/text()').extract_first()
        # photo = response.xpath("//div[contains(@class,'gallery-img-wrapper')]/div[contains(@class,'gallery-img-frame')]/@data-url").extract()
        # yield AvitoparserItem(name=name,photo=photo,price=price)



