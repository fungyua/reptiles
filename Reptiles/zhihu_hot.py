import json
import re

import pymongo
import requests

from config.config import mongo, headers


class zhihu_hot:
    def __init__(self):
        self.url = 'https://www.zhihu.com/billboard'
        collection_name = 'zhihu'
        self.db = pymongo.MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))[mongo.get('database')]
        self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names():
            print('集合已经存在')
            self.collection.drop()
            print('集合已经删除')

    def run(self):
        result = json.loads(
            re.search(r'(?<="hotList":).+?]', requests.get(self.url, headers=headers).text).group())
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
            i += 1
            self.collection.insert_one(topic)
        print('爬取完毕')


if __name__ == '__main__':
    zhihu_hot().run()
