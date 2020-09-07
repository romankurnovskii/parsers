import locale

from ParseJobs import DB, HeadHunter
from ParseJobs import Superjob

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')



# create entires
superjob = Superjob()
headhunter = HeadHunter()

#
response = input("Введите вакансию")
sj_vacs = superjob.getVacancies(response)
hh_vacs = headhunter.getVacancies(response)


# insert into db
DB.insertSuperjob(sj_vacs)
DB.insertHeadhunter(hh_vacs)
