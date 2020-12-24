from pymongo import MongoClient
from requests import get

from config import mongo, headers


class MaoYan:
    def __init__(self):
        self.url = 'https://piaofang.maoyan.com/dashboard'
        self.json = 'https://piaofang.maoyan.com/dashboard-ajax/movie'
        collection_name = 'maoyan'
        self.client = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))
        self.db = self.client[mongo.get('database')]
        self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names():
            print('数据表已存在')
            self.collection.drop()
            print('数据表已删除')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and exc_val and exc_tb:
            print(exc_type, exc_val, exc_tb)
        self.client.close()
        print('已断开数据库连接')

    def run(self):
        data = get(self.json, headers=headers, params={
            'orderType': 0,
            'uuid': '378b8d60-4c00-4bf8-9604-3188c2f39cba',
            'riskLevel': 71,
            'optimusCode': 10,
            '_token': 'eJydklFrwjAQx7%2FLPYf2rqlpEvChMBgVfJioL%2BJDtF0to420RTaG392LbODbViFwv'
                      '%2Fz55TiOfENflGBRwKXqwQJFGCkQMA5gSaHWNCMlZ8YIOD5mmaRECjj02xewO1ZSYZTZh2TFwY5MgoJQ4148skQ'
                      '%2BwSpYgtM4ngcbx%2BfG%2BXfX1VHr%2FJfroqNv49INp4N3fRm3%2FtJUPNK%2FbODm7To0J0ISqUr5JZGUjDqgQiVSI'
                      '%2B8YUpNNx2QC0nOIf2BiJqB%2BDrM78kI%2FwkK5up86%2Ft6X%2FGPYHZq6Y6oWn%2BtNXeT5a52v3uZzuN4AiTWMOg'
                      '%3D%3D '
        })
        for i in data.json()['movieList']['list']:
            self.collection.insert_one(i)


if __name__ == '__main__':
    MaoYan().run()
