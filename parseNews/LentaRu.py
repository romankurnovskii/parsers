import requests
from lxml import html


class LentaRu:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        self.url = 'https://lenta.ru/'

    def connect(self):
        response = requests.get(self.url, headers=self.header)
        dom = html.fromstring(response.text)
        self.links = dom.xpath("//div[@class='item']//a[not(@class)]/@href")

    def __linkToStr(self, url):
        response = requests.get(url, headers=self.header)
        dom = html.fromstring(response.text)
        return dom

    def __parseTitle(self, dom):
        title = dom.xpath("//h1[@class='common-head__title']")
        if len(title) == 0:
            title = dom.xpath("//h1[@class='b-topic__title']")
        return title[0].text

    def __parseDateTime(self, dom):
        datetime = dom.xpath("//time[@class='g-date']/@datetime")
        if datetime is None:
            datetime = dom.xpath("//time[@class='common-head__info-text']")
        return datetime[0]

    def parse(self):
        res = []
        for e in self.links:
            url = self.url + e
            dom = self.__linkToStr(url)

            res.append({
                'date': self.__parseDateTime(dom),
                'title': self.__parseTitle(dom),
                'url': url

            })
        return res
