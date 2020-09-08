import datetime

def convertMonthToNum(month_name):
    month_name = month_name[0:3]
    # long_month_name = "Июн"
    datetime_object = datetime.datetime.strptime(month_name, "%b")
    month_number = datetime_object.month
    return month_number

def convertSalary(salary):
    if salary == None:
        return {'мин': None, 'макс': None, 'валюта': None}
    salary = salary.getText()
    try:
        salary = int(salary)
        if salary >= 0:
            return {'мин': salary, 'макс': salary, 'валюта': None}
    except:
        pass

    if salary == 'По договорённости':
        return {'мин': None, 'макс': None, 'валюта': None}

    salary = salary.replace('\xa0', '')

    if 'от' in salary:
        salary = salary.split('от')
        currency = None
        if 'руб' in salary[1]:
            currency = 'руб'
            salary = salary[1].split('руб')
        if 'KZT' in salary[1]:
            currency = 'KZT'
            salary = salary[1].split('KZT')
        min = int(salary[0])
        salary = {'мин': min, 'макс': None, 'валюта': currency}
        return salary

    if 'до' in salary:
        salary = salary.split('до')
        currency = None
        if 'руб' in salary[1]:
            currency = 'руб'
            salary = salary[1].split('руб')
        if 'KZT' in salary[1]:
            currency = 'KZT'
            salary = salary[1].split('KZT')
        max = int(salary[0])
        salary = {'мин': None, 'макс': max, 'валюта': currency}
        return salary

    if '—' in salary:
        salary = salary.split('—')
        min = int(salary[0])
        currency = None
        if 'руб' in salary[1]:
            currency = 'руб'
            salary = salary[1].split('руб')
        if 'KZT' in salary[1]:
            currency = 'KZT'
            salary = salary[1].split('KZT')
        max = int(salary[0])
        salary = {'мин': min, 'max': max, 'валюта': currency}
        return salary

    if '-' in salary:
        salary = salary.split('-')
        min = int(salary[0])
        currency = None
        if 'руб' in salary[1]:
            currency = 'руб'
            salary = salary[1].split('руб')
        if 'KZT' in salary[1]:
            currency = 'KZT'
            salary = salary[1].split('KZT')
        max = int(salary[0])
        salary = {'мин': min, 'max': max, 'валюта': currency}
        return salary