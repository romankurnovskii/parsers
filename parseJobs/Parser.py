import locale
from pprint import pprint

import DB
from HeadHunter import HeadHunter
from Superjob import Superjob

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# create entires
superjob = Superjob()
headhunter = HeadHunter()

#
response = input("Введите вакансию: ")
print('Loading...')
sj_vacs = superjob.getVacancies(response)
hh_vacs = headhunter.getVacancies(response)

pprint(sj_vacs)

# insert into db
DB.insertSuperjob(sj_vacs)
DB.insertHeadhunter(hh_vacs)
