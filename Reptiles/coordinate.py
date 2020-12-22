from lxml import etree
from pymongo import MongoClient
from requests import get

from config import mongo, headers
from xpinyin import Pinyin
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


class Coordinate:
    def __init__(self, collection_name, pages):
        self.url = 'http://www.hao828.com/chaxun/zhongguochengshijingweidu/'
        self.drive = 'redis'
        self.p = Pinyin()
        self.client = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))
        self.db = self.client[mongo.get('database')]
        self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names():
            print('数据表已存在')
            self.collection.drop()
            print('已删除数据表')
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_data, list(range(1, pages + 1)))

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭数据库连接')
        self.client.close()

    def get_data(self, page):
        data = etree.HTML(get(self.url, headers=headers, params={'PageNo': page}).text).xpath('//*[@id="content"]/table[3]/tr')
        for i in data[1:]:
            td = i.xpath('./td')
            topic = {
                'province': td[1].text,
                'provincePinyin': self.p.get_pinyin(td[1].text, ''),
                'city': td[3].text,
                'pinyin': td[4].text,
                'areaCode': td[5].text,
                'postCode': td[6].text,
                'longitude': float(td[7].text),
                'latitude': float(td[8].text)
            }
            self.collection.insert_one(topic)
            print(f'{td[3].text} 已存入数据库')


if __name__ == '__main__':
    Coordinate(collection_name='coordinate', pages=125)
