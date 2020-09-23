import scrapy
from scrapy.http import HtmlResponse
from parseJobsScrapy.items import ParsejobsscrapyItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://samara.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response: HtmlResponse):
        vacancies_urls = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()
        for vacancy in vacancies_urls:
            yield response.follow(vacancy, callback=self.vacancy_parse)

        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        print()

    def vacancy_parse(self, response: HtmlResponse):
        url = response.url
        title = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        yield ParsejobsscrapyItem(title=title, salary=salary, url=url)
