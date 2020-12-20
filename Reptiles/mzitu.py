import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from config import mongo, headers


class mzitu:
    image_path = ''

    def __init__(self, root, page=1, min_time=0, max_time=1):
        self.url = f'https://www.mzitu.com/page/{page}'
        self.root = root
        headers['referer'] = 'https://www.mzitu.com/'
        collection_name = 'mzitu'
        self.db = MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                mongo.get('user'), mongo.get('password'), mongo.get('host'),
                mongo.get('port')))[mongo.get('database')]
        self.collection = self.db[collection_name]
        self.min_time = min_time
        self.max_time = max_time
        if collection_name in self.db.list_collection_names():
            print('集合已经存在')
            self.collection.drop()
            print('集合已经删除')

    def run(self):
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_images,
                       BeautifulSoup(requests.get(self.url, headers=headers).text, 'lxml').find('ul',
                                                                                                id='pins').find_all(
                           'li'))

    def get_images(self, data):
        image = data.find('img')
        self.image_path = f'{self.root}/{image.get("alt")}'
        os.makedirs(self.image_path, exist_ok=True)
        self.save_image(image.get('data-original'), '_avatar')
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.submit(self.get_image, data.find('a').get('href'))

    def get_image(self, url):
        self.save_image(
            BeautifulSoup(requests.get(url, headers=headers).text, 'lxml').find('img', class_='blur').get('src'), '1')

    def save_image(self, url, file_name='only'):
        with open(f'{self.image_path}/{file_name}{os.path.splitext(url)[1]}', 'wb') as f:
            f.write(requests.get(url, headers=headers).content)
            print(f'成功下载 {url}')
            time.sleep(random.randint(self.min_time, self.max_time))


if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0] + '/images'
    mzitu(current_path).run()
