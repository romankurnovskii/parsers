# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from leroymerlinparser.items import LeroymerlinparserItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, req):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={req}']

    def parse(self, response):
        next_page = response.xpath("//div[@class='service-panel clearfix']//a[contains(@class,'next-paginator-button')]/@href").extract_first()
        product_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)
        yield response.follow(next_page, callback=self.parse)


    def parse_product(self, response):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('_id', '//div[@class="product-detailed-page"]/@data-product-id')
        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('photo', '//picture/source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        loader.add_xpath('price', '//uc-pdp-price-view[@slot="primary-price"]//meta[@itemprop="price"]/@content')
        loader.add_xpath('currency', '//uc-pdp-price-view[@class="primary-price"]/meta[@itemprop="priceCurrency"]/@content')
        loader.add_xpath('unit', '//uc-pdp-price-view[@class="primary-price"]/meta[@itemprop="availability"]/@content')
        blocks = response.xpath('//dl[@class="def-list"]/div[@class="def-list__group"]')
        loader.add_value('characteristics', blocks)
        loader.add_value('link', response.url)
        yield loader.load_item()