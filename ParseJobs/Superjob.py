from bs4 import BeautifulSoup as bs
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


class Superjob:
    def __init__(self):
        self.name = "Supejob"
        self.mainUrl = "https://www.russia.superjob.ru"
        self.searchUrl = "https://russia.superjob.ru/vacancy/search/?"
        self.dictionary = []

    def makeUrl(self):
        response = requests.get(self.url)
        soup = bs(self.mainUrl)
        return soup

    # последняя ли страница
    def isLastPage(self, soup):
        res = soup.find('span', text='Дальше')
        if res != None:
            return False
        return True

    def getVacancies(self, keywords, limit=30):
        self.parse(keywords, limit)
        return self.dictionary

    def parse(self, keywords, limit):
        pageNumber = 0

        url = self.searchUrl + 'keywords=' + keywords + '&page=' + str(pageNumber)
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'html.parser')

        while limit > 0 & self.isLastPage(soup):

            url = self.searchUrl + 'keywords=' + keywords + '&page=' + str(pageNumber)
            response = requests.get(url, headers=headers)
            soup = bs(response.text, 'html.parser')

            cards = soup.select("div.iJCa5.f-test-vacancy-item")

            for card in cards:
                salary = card.findChild('span', attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
                name = card.findChild('a', attrs={'class': '_6AfZ9'})
                link = card.findChild('a', {'class': '_1UJAN'}, href=True)
                employer = card.select_one('.icMQ_._205Zx')
                location = card.select('span.f-test-text-company-item-location')
                datePublished = card.findChild('span', attrs={'class': '_3mfro _9fXTd _2JVkc _2VHxz'})

                link = self.mainUrl + link['href']
                location = location[0].findChild('span', attrs={'class': ''}).getText()
                if employer is not None:
                    employer = employer.getText()

                salary = self.convertSalary(salary)

                self.dictionary.append({
                    'name': name.getText(),
                    'salary': salary,
                    'joblink': link,
                    'employer': employer,
                    'location': location,
                    'datePublished': datePublished.getText()
                })

                limit -= 1
                if limit == 0:
                    break

            pageNumber += 1


    def convertSalary(self, salary):
        try:
            salary = int(salary)
            if salary >= 0:
                return salary
        except:
            salary = salary.getText()

        if salary == 'По договорённости':
            return None

        salary = salary.replace('\xa0', '')

        if 'от' in salary:
            salary = salary.split('от')
            salary = salary[1].split('руб')
            min = int(salary[0])
            currency = 'руб'
            salary = {'мин': min, 'валюта': currency}
            return salary

        if 'до' in salary:
            salary = salary.split('до')
            salary = salary[1].split('руб')
            max = int(salary[0])
            currency = 'руб'
            salary = {'макс': max, 'валюта': currency}
            return salary

        if '—' in salary:
            salary = salary.split('—')
            min = int(salary[0])
            salary = salary[1].split('руб')
            max = int(salary[0])
            currency = 'руб'
            salary = {'мин': min, 'max': max, 'валюта': currency}
            return salary
