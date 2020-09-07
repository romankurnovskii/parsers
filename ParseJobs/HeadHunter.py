class HeadHunter:
    def __init__(self):
        self.name = "HeadHunter"
        self.mainUrl = "https://hh.ru/"
        self.searchUrl = "https://hh.ru/search/vacancy?text="
        self.dictionary = []

    def makeUrl(self):
        response = requests.get(self.url)
        soup = bs(self.mainUrl)
        return soup

    # последняя ли страница
    def isLastPage(self, soup):
        res = soup.find('a', text='Дальше')  # bloko-button HH-Pager-Controls-Next HH-Pager-Control
        if res != None:
            return False
        return True

    def getVacancies(self, keywords, limit=50):
        self.parse(keywords, limit)
        pprint(self.dictionary)

    def parse(self, keywords, limit):
        pageNumber = 1

        url = self.searchUrl + keywords + '&page=' + str(pageNumber)
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'html.parser')

        while limit > 0 & self.isLastPage(soup):

            url = self.searchUrl + keywords + '&page=' + str(pageNumber)
            response = requests.get(url, headers=headers)
            soup = bs(response.text, 'html.parser')

            cards = soup.select("div.vacancy-serp-item")

            for card in cards:
                salary = card.findChild('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                name = card.findChild('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
                link = card.findChild('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}, href=True)
                employer = card.findChild('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                location = card.findChild('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
                datePublished = card.findChild('span', attrs={'class': 'vacancy-serp-item__publication-date'})

                link = link['href']
                location = location.getText()
                if employer is not None:
                    employer = employer.getText()
                if salary is not None:
                    salary = salary.getText()

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
                # print([name.getText(), salary.getText(), link, employer, location,
                #        datePublished.getText()])

            pageNumber += 1