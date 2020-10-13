# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from cian.items import CianItem
###_Подключаем Селениум_####
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.loader import ItemLoader

class CianruSpider(scrapy.Spider):
    name = 'cianru'
    allowed_domains = ['cian.ru']
    start_urls = ['https://izhevsk.cian.ru/kupit/']  #Стартуем сразу с раздела продаж

    def parse(self, response: HtmlResponse):
        #На стартовой странице ищем блок с ссылками, за которые можно зацепиться
        #Находим ссылки в графе полезные ссылки справа
        categories_page = response.xpath("//div[@class='c-popular-links']//a[@data-name]/@href").extract()
        for url in categories_page: #Ссылок много, поэтому обрабатываем их всех
            yield response.follow(url, callback=self.ads_rows_parse) #Через yield

    def ads_rows_parse(self, response: HtmlResponse):  #Ищем ссылки на следующие страницы
        paginator = response.xpath("//div/ul//li[contains(@class,'list-item')]/a/@href").extract()

        for page_url in paginator: #И переходим по этим ссылкам, получая страницы с квартирами
            yield response.follow(page_url, callback=self.ads_rows_parse)

        #Ищем ссылки на квартиры в открывшейся странице
        ads_links = response.xpath("//div[contains(@class,'--card--')]//a[contains(@class,'header')]/@href").extract()

        for link in ads_links:  #Заходим внутрь каждой ссылки
            yield response.follow(link, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse): #Тут обрабатываем каждое объвление
        loader = ItemLoader(item=CianItem(), response=response)
        loader.add_xpath('name','//h1/text()')   #Наименование объявления
        loader.add_xpath('price',"//span[@itemprop='price']/text()") #Цена квартиры

        # А вот тут досада :( Фотки грузятся динамически, поэтому селениум
        driver = webdriver.Chrome()     #Для каждого объявления создаем свой объект, и свое окно с браузером
        actions = ActionChains(driver)  #чтобы пришедшее объявление из другого потока не переписало нашу страницу
        driver.get(response.url)        #Открываем текущее объявление в селениуме

        thumbs = WebDriverWait(driver,10).until(   #Прогружаем превьюхи
            EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class,'fotorama__nav__frame fotorama__nav__frame--thumb')]"))
        )
        actions.move_to_element(thumbs[-1]).click().perform() #Переходим к последней, чтобы прогрузить все превьюхи

        photos = [i.find_element_by_xpath(".//img").get_attribute('src') for i in thumbs] #Извлекаем из каждого объекта ссылку на фотку
        #Извлечь атрибуты именно здесь нужно, опять же из-за селениума. Поэтому на фотках чуть тормозим формируя уже готовый список ссылок
        driver.quit()
        photos.pop()  #Ну я не удержался выкинуть тут последнюю фотку с рекламой об ипотеке :) Она есть везде.

        loader.add_value('photos',photos) #Фотки готовые поэтому просто добавляем это значение к лоадеру
        yield loader.load_item() #Кидаем в item


