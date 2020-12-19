import os
import pymongo
import requests
from lxml import etree
from config.config import mongo, headers


def main():
    html = etree.HTML(requests.get(url, headers).content.decode('utf-8'))
    ls = html.xpath('/html/body/div[4]/div[1]/div/div[2]/ul[1]/li/a')
    topics = []
    i = 1
    for target in ls:
        topic = {
            '_id': i,
            'title': target.xpath('.//i')[0].text,
            'url': target.get('href'),
            'time': target.xpath('.//em')[0].text,
            'image': target.get('rel')
        }
        topics.append(topic)
        i = i + 1
    return topics


if __name__ == '__main__':
    url = 'https://www.lssdjt.com/'
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
