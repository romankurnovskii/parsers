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
