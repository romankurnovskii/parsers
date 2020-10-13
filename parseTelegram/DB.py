from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['telegram_users']  # database

telegram_users = db.telegramUsers


def insertIntoMongoDB(users):
    for user in users:
        if not isExists(telegram_users, user):
            telegram_users.insert_one(user)

def isExists(collection, user):
    count = collection.find({'id': user['id']}).count()
    if count > 0:
        return True
    return False