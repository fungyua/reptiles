from bs4 import BeautifulSoup as Bs
from pymongo import MongoClient
from requests import get

from config import headers, mongo

from concurrent.futures import ThreadPoolExecutor


class V2ex:
    def __init__(self):
        collection_name = 'v2ex'
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
        page = Bs(get('https://www.v2ex.com/go/android', headers=headers).text, 'lxml').select('#TopicsNode tr')
        with ThreadPoolExecutor(8) as thread:
            thread.map(self.get_page, page)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_page(self, data):
        title_link = data.find(class_='topic-link')
        avatar_el = data.find(class_='avatar')
        last_answers_el = data.select_one('.topic_info strong:last-child a')
        topic = {
            'title': title_link.text,
            'sourceUrl': title_link.get('href'),
            'author': {
                'name': avatar_el.get('alt'),
                'link': data.find('a').get('href'),
                'avatar': avatar_el.get('src')
            },
            'public_time': data.select_one('.topic_info span').text,
            'answers': None if last_answers_el is None else {
                'count': data.select_one('td:last-child a').text,
                'last': {
                    'author': last_answers_el.text,
                    'link': last_answers_el.get('href'),
                }
            }
        }
        self.collection.insert_one(topic)
        print('已插入 %s' % topic['title'])


if __name__ == '__main__':
    V2ex()
