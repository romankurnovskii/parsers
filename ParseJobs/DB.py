from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['jobs']  # database

headhunter = db.headhunter
superjob = db.superjob


def insertSuperjob(object):
    for vacancy in object:
        if not isExists(superjob, vacancy):
            superjob.insert_one(vacancy)


def insertHeadhunter(object):
    for vacancy in object:
        if not isExists(headhunter, vacancy):
            headhunter.insert_one(vacancy)

# find vacancies where salary greater then input
def salary_query(collection, salary):
    # client = MongoClient('localhost', 27017)
    # db = client['jobs']
    # collection = db.get_collection(collection)
    result = []
    for job in collection.find(
            {'$or': [{'min_salary': {'$lt': salary}}, {'max_salary': {'$gt': salary}}]}
    ):
        result.append(job)

    return result


#check if vacancy excists in database
def isExists(collection, object):
    #check by link
    count = collection.find({'joblink': object['joblink']}).count()
    if count > 0:
        return True
    return False
