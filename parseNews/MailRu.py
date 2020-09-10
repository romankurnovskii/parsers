import requests
from lxml import html


class MailRu:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        self.url = 'https://news.mail.ru/'

    def connect(self):
        response = requests.get(self.url, headers=self.header)
        dom = html.fromstring(response.text)
        self.links = self.__parseLinks(dom)

    def __parseLinks(self, dom):
        links = []
        # get link from Main
        # links.append(dom.xpath(
        #     "//a[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/@href"))

        # # get links from header photos
        links += dom.xpath("//a[@class='photo photo_small photo_scale photo_full js-topnews__item']/@href")

        # # get links from ul string
        links += dom.xpath("//a[@class='list__text']/@href")

        return links

    def __linkToStr(self, url):
        response = requests.get(url, headers=self.header)
        dom = html.fromstring(response.text)
        return dom

    def __parseTitle(self, dom):
        title = dom.xpath("//h1[@class='hdr__inner']")
        return title[0].text

    def __parseDateTime(self, dom):
        datetime = dom.xpath("//span[contains(@datetime,2020)]/@datetime")
        if datetime is None:
            return None
        return datetime[0]

    def parse(self):
        res = []
        for e in self.links:
            if 'http' in e:
                url = e
            else:
                url = self.url + e
            dom = self.__linkToStr(url)

            res.append({
                'date': self.__parseDateTime(dom),
                'title': self.__parseTitle(dom),
                'url': url

            })
        return res
