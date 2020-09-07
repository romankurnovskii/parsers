from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['jobs']  # database

headhunter = db.headhunter
superjob = db.superjob


def insertSuperjob(object):
    for vacancy in object:
        superjob.insert_one(vacancy)

def insertHeadhunter(object):
    for vacancy in object:
        headhunter.insert_one(vacancy)


def salary_query(collection, max):
    client = MongoClient('localhost', 27017)
    db = client['jobs']
    collection = db.get_collection(collection)
    for job in collection.find(
            {'$or': [{'min_salary': {'$lt': max}}, {'max_salary': {'$gt': max}}]}
    ):
        print(job)