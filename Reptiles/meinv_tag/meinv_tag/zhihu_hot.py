import requests
import pymongo
import re
import json
import configparser
import os
import pymysql


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


def config(filepath):
    cnf = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + filepath
    cnf.read(path)
    return cnf


if __name__ == '__main__':
    url = 'https://www.zhihu.com/billboard'
    collectionName = 'zhihu'
    config = config('/db/config.conf')
    drive = 'mongo'

    client = pymongo.MongoClient(
        "mongodb://%s:%s@%s:%s" % (
            config.get(drive, 'user'), config.get(drive, 'password'), config.get(drive, 'host'),
            config.get(drive, 'port')))
    db = client[config.get(drive, 'database')]
    collection = db[collectionName]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 '
    }
    if collectionName in db.list_collection_names():
        print('集合已经存在')
        client[dbName][collectionName].drop()
        print('集合已经删除')
    client[dbName][collectionName].insert_many(main())
    print('爬取完毕')
