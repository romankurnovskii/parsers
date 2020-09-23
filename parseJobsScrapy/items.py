# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ParsejobsscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()

    _id = scrapy.Field() #для монго бд, она автоматом создает поле
