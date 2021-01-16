import json
import re

from pymongo import MongoClient
import requests

from config import mongo, headers


class zhihu_hot:
    def __init__(self):
        self.url = 'https://www.zhihu.com/billboard'
        collection_name = 'zhihu'
        self.client = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))
        self.db = self.client[mongo.get('database')]
        self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names():
            print('集合已经存在')
            self.collection.drop()
            print('集合已经删除')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭数据库连接')
        self.client.close()

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
