import random
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from config import mongo, params


class ExHentai:
    def __init__(self, options=params, page=0):
        self.headers = options['headers']
        self.cookies = options['cookie']
        self.data = requests.get(options['url'], params={'page': page}, headers=self.headers, cookies=self.cookies)
        self.db = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('passwd'), mongo.get('host'),
                mongo.get('port'))).get(mongo.get('db'))
        self.collection = self.db.get(mongo.get('table'))
        self.get_data()

    def get_data(self):
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_url,
                       BeautifulSoup(self.data.text, 'lxml').find('table', class_='itg').find_all('tr')[1:3])

    def get_url(self, data):
        link = data.find('td', class_='gl3c').a
        img = data.find('img')
        topic = {
            'title': img['alt'],
            'link': link['href'],
            'img': img.get('data-src', img['src'])
        }
        self.collection.insert_one(topic)
        self.get_images(topic)
        time.sleep(random.randint(1, 3))
        print('插入成功%s' % topic['title'])

    def get_images(self, data):
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_image,
                       BeautifulSoup(requests.get(data['link']).text, 'lxml').find('div', id='gdt').find_all('a'))

    def get_image(self, data):
        print(BeautifulSoup(requests.get(data['href']).text, 'lxml').find('img', id='img')['src'])
        time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    pages = list(range(2))
    with ProcessPoolExecutor(max_workers=len(pages)) as process:
        process.map(ExHentai, pages)
