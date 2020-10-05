import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import re


def convert_to_int(num):
    if num:
        return int(num)


def convert_to_float(num):
    if num:
        num = num.replace(" ", "")
        return float(num)


def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value


def split_characteristics(value):
    characteristic = {}
    try:
        characteristic['name'] = value.xpath(
            './dt[@class="def-list__term"]/text()').extract_first()
        characteristic['value'] = formatting_string(
            value.xpath('./dd[@class="def-list__definition"]/text()').extract_first())
    except Exception as ex:
        print(f'split_characteristics - {ex}')
    return characteristic


def formatting_string(string):
    if string:
        res = re.sub('^\s+|\n|\r|\s+$', '', string)
        return res


class LeroymerlinparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor=MapCompose(
        convert_to_float), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field(
        input_processor=MapCompose(split_characteristics))
    _id = scrapy.Field(input_processor=MapCompose(
        convert_to_int), output_processor=TakeFirst())
