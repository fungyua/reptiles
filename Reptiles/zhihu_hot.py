import json
import re

import pymongo
import requests

from config.config import mongo


# from openpyxl import writer, workbook


def main():
    topics = []
    result = json.loads(
        re.search(r'(?<="hotList":).+?]', requests.get(url, headers=headers).text).group())
    i = 1
    for x in result:
        target = x['target']
        topic = {
            '_id': i,
            'title': target['titleArea']['text'],
            'image': target['imageArea']['url'],
            'hot': target['metricsArea']['text'],
            'url': target['link']['url'],
            'desc': target['excerptArea']['text']
        }
        i = i + 1
        topics.append(topic)
    return topics


if __name__ == '__main__':
    url = 'https://www.zhihu.com/billboard'
    collectionName = 'zhihu'

    client = pymongo.MongoClient(
        "mongodb://%s:%s@%s:%s" % (
            mongo.get('user'), mongo.get('password'), mongo.get('host'),
            mongo.get('port')))
    db = client[mongo.get('database')]
    collection = db[collectionName]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 '
    }
    if collectionName in db.list_collection_names():
        print('集合已经存在')
        collection.drop()
        print('集合已经删除')
    collection.insert_many(main())
    print('爬取完毕')
