import pymongo
import requests
from bs4 import BeautifulSoup
from config import mongo, headers


def main():
    topics = []
    i = 1
    for target in BeautifulSoup(requests.get(url, headers).content.decode('utf-8'), 'lxml').select('.list a'):
        topic = {
            '_id': i,
            'title': target['title'],
            'url': url + target['href'],
            'time': target.find('em').text,
            'image': target.get('rel')
        }
        topics.append(topic)
        i = i + 1
    return topics


if __name__ == '__main__':
    url = 'https://www.lssdjt.com'
    collectionName = 'today'
    drive = 'mongo'

    client = pymongo.MongoClient(
        "mongodb://%s:%s@%s:%s" % (
            mongo.get('user'), mongo.get('password'), mongo.get('host'),
            mongo.get('port')))
    db = client[mongo.get('database')]
    collection = db[collectionName]

    if collectionName in db.list_collection_names():
        print('集合已经存在')
        db[collectionName].drop()
        print('集合已经删除')
    collection.insert_many(main())
    print('爬取完毕')
