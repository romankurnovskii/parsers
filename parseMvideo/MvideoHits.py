from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


class MvideoHits:
    def __init__(self):
        self.__URL = 'https://www.mvideo.ru/'
        self.__driver = ''
        self.__dictionary = []

    def start(self):
        self.__connect()
        hits = self.__parseHits()
        self.__dictionary += self.__convertToObjexts(hits)

    def __connect(self):
        self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver.get(self.__URL)

    def __parseHits(self):
        hits_block = self.__driver.find_element_by_xpath(
            "//div[contains(text(),'Хиты продаж')]/ancestor::div[@data-init='gtm-push-products']")
        wait = WebDriverWait(hits_block, 10)
        hits = ''
        while True:
            try:
                nextButton = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')))
                self.__driver.execute_script("$(arguments[0]).click();", nextButton)
            except:
                hits = hits_block.find_elements_by_css_selector('li.gallery-list-item')
                break
        return hits

    def __convertToObjexts(self, elements):
        list = []
        for el in elements:
            res = self.__getElementInfo(el)
            list.append(res)
        return list

    def __getElementInfo(self, element):
        el = {}
        el['title'] = element.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('innerHTML')
        el['url'] = element.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')
        el['price'] = float(
            element.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerHTML').replace(
                '&nbsp;', '').replace('¤', ''))
        el['img'] = element.find_element_by_css_selector(
            'img[class="lazy product-tile-picture__image"]').get_attribute('src')
        return el

    def getProducts(self):
        return self.__dictionary
