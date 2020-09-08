import locale
from pprint import pprint

from ParseJobs import DB
from ParseJobs.HeadHunter import HeadHunter
from ParseJobs.Superjob import Superjob

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# create entires
superjob = Superjob()
headhunter = HeadHunter()

#
response = input("Введите вакансию")
sj_vacs = superjob.getVacancies(response)
hh_vacs = headhunter.getVacancies(response)

pprint(sj_vacs)

# insert into db
DB.insertSuperjob(sj_vacs)
DB.insertHeadhunter(hh_vacs)
