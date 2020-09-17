import json
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
# wait until page loads
options.page_load_strategy = 'eager'

class MailRu:
    def __init__(self):
        self.URL = 'http://mail.ru'
        self.__dictionary = []

    def __getCredentials(self):
        f = open('config.json', )
        data = json.load(f)
        self.__login = data['login']
        self.__pass = data['password']
        self.__domain = data['domain']

    def __connect(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.URL)

        login_name = self.driver.find_element_by_id('mailbox:login-input')
        login_name.send_keys(self.__login)

        login_domain = self.driver.find_element_by_id('mailbox:domain')
        domain = Select(login_domain)
        domain.select_by_visible_text(self.__domain)

        submit = self.driver.find_element_by_id('mailbox:submit-button')
        submit.send_keys(Keys.RETURN)
        print('loading data...')
        sleep(5)

        pass_input = self.driver.find_element_by_id('mailbox:password-input')
        pass_input.send_keys(self.__pass)
        submit.send_keys(Keys.RETURN)
        print('submitting data...')
        sleep(10)
        print('...')

    def start(self, countEmails=50):
        self.__getCredentials()
        self.__connect()
        self.__parse(countEmails)
        self.driver.close()

    def __parse(self, countEmails):
        actions = ActionChains(self.driver)
        while True:
            actions.send_keys(Keys.ARROW_DOWN).perform()
            element = self.driver.switch_to.active_element
            attrs = self.__getElementInfo(element)
            self.__dictionary.append(attrs)
            countEmails -= 1
            if countEmails == 0:
                break


    def __getElementInfo(self, element):
        id = element.get_attribute('data-uidl-id')
        title = element.find_element_by_class_name('ll-sj__normal').text
        link = element.get_attribute('href')
        date = element.find_element_by_class_name('llc__item_date').get_attribute('title')
        return {
            "id": id,
            "title": title,
            "link": link,
            "date": date
        }

    def getEmails(self):
        print('в базе: ', len(self.__dictionary), ' элементов')
        for el in self.__dictionary:
            print(el)
