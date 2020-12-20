from lxml import etree
from pymongo import MongoClient
from requests import get

from config import mongo, headers


class Coordinate:
    def __init__(self):
        self.url = 'http://www.hao828.com/chaxun/zhongguochengshijingweidu/'
        self.pages = 2493
        collection_name = 'coordinate'
        self.db = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))[mongo.get('database')]
        self.collection = self.db[collection_name]
        if collection_name in self.db.list_collection_names():
            print('表已存在')
            self.collection.drop()
            print('已删除表')
        for i in range(self.pages):
            self.get_data(i)

    def get_data(self, page):
        data = etree.HTML(get(self.url, headers=headers, params={'PageNo': page}).text).xpath('//*[@id="content"]/table[3]/tr')
        for i in data[1:]:
            td = i.xpath('./td')
            topic = {
                'province': td[1].text,
                'city': td[3].text,
                'pinyin': td[4].text,
                'areaCode': td[5].text,
                'postCode': td[6].text,
                'longitude': td[7].text,
                'latitude': td[8].text
            }
            print(f'{td[3].text} 已存入数据库')
            self.collection.insert_one(topic)


if __name__ == '__main__':
    Coordinate()
