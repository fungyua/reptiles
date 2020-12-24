from requests import Session, post
from urllib.parse import quote
from config import headers, mongo
from pymongo import MongoClient
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


class Lago:
    # 初始化
    def __init__(self, word):
        collection_name = 'lago'
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.word = word
        self.headers = dict({
            'Host': 'www.lagou.com',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'https://www.lagou.com/jobs/list_{quote(self.word)}?labelWords=&fromSearch=true&suginput='
        }, **headers)
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
        s = Session()
        self.pages = s.get(url=self.headers.get('Referer'), headers=self.headers, timeout=10)
        self.cookies = s.cookies

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭数据库连接')
        self.client.close()

    def get_data(self, page):
        res = post(self.url, headers=self.headers, data={
            'first': 'true',
            'pn': page,
            'kd': self.word
        }, cookies=self.cookies, timeout=3)
        res.encoding = 'utf-8'
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.insert, res.json()['content']['positionResult']['result'])

    def insert(self, data):
        topic = {
            'city': data['city'],
            'companyFullName': data['companyFullName'],
            'companyLogo': data['companyLogo'],
            'companyShortName': data['companyShortName'],
            'companySize': data['companySize'],
            'createTime': data['createTime'],
            'district': data['district'],
            'education': data['education'],
            'financeStage': data['financeStage'],
            'linestaion': data['linestaion'],
            'longitude': data['longitude'],
            'latitude': data['latitude'],
            'firstType': data['firstType'],
            'industryField': data['industryField'],
            'positionAdvantage': data['positionAdvantage'],
            'positionLables': data['positionLables'],
            'positionName': data['positionName'],
            'salary': data['salary'],
            'workYear': data['workYear']
        }
        self.collection.insert_one(topic)
        print(topic.get('positionName') + '已插入数据库')

    def run(self):
        print(self.pages)


if __name__ == '__main__':
    Lago(word='python').run()
