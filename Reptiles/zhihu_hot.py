import requests
import pymongo
import re
import json
import configparser
import os
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


def config(filePath):
    cnfObj = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + filePath
    cnfObj.read(path)
    return cnfObj


if __name__ == '__main__':
    url = 'https://www.zhihu.com/billboard'
    dbName = 'reptiles'
    collectionName = 'zhihu'
    config = config('/db/config.conf')

    client = pymongo.MongoClient(
        "mongodb://%s:%s" % (config.get('mongo', 'dbHost'), config.get('mongo', 'dbPort')))
    db = client[config.get('mongo', 'dbName')]
    collection = db[collectionName]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
    }
    if collectionName in client[dbName].list_collection_names():
        print('集合已经存在')
        client[dbName][collectionName].drop()
        print('集合已经删除')
    client[dbName][collectionName].insert_many(main())
    print('爬取完毕')
