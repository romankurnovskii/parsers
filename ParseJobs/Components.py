import datetime

def convertMonthToNum(month_name):
    month_name = month_name[0:3]
    # long_month_name = "Июн"
    datetime_object = datetime.datetime.strptime(month_name, "%b")
    month_number = datetime_object.month
    return month_number