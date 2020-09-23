# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class ParsejobsscrapyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.hh_ru_scrapy

    def process_item(self, item, spider):
        title = item['title']
        salary = self.convert_salary(item['salary'])
        url = item['url']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def convert_salary(self, salary):
        if salary == None or 'з/п не указана' in salary[0] or 'По договорённости' in salary[0] :
            return {'мин': None, 'макс': None, 'валюта': None}

        if 'от' in salary[0] and len(salary) > 5:
            min = int(salary[1].replace('\xa0', ''))
            max = int(salary[3].replace('\xa0', ''))
            return {'мин': min, 'макс': max, 'валюта': salary[5]}

        if 'от' in salary[0] and len(salary) >= 4:
            return {'мин': salary[1].replace('\xa0', ''), 'макс': None, 'валюта': salary[3]}

        if 'до' in salary[0]:
            min = int(salary[1].replace('\xa0', ''))
            return {'мин': min, 'макс': None, 'валюта': salary[3]}