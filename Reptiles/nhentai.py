from config import headers, mongo
from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
from time import sleep
from random import randint
import os
import re


class NHenTai:
    def __init__(self, min_time=0, max_time=1):
        self.url = 'https://nhentai.net'
        self.min_time = min_time
        self.max_time = max_time
        self.client = MongoClient(
            f"mongodb://{mongo.get('user')}:{mongo.get('password')}@{mongo.get('host')}:{mongo.get('port')}")
        self.collection_name = 'nhentai'
        self.db = self.client[mongo.get('database')]
        self.collection = self.db[self.collection_name]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def run(self):
        if self.collection_name in self.db.list_collection_names():
            print('数据表已存在')
            self.collection.drop()
            print('数据表已删除')
        for i in self.get_page(1):
            data = BeautifulSoup(get(self.url + i.find("a")["href"], headers=headers).text, 'lxml')
            info = data.find('div', id='info')
            topic = {
                'id': list(info.find('h3', id='gallery_id').strings)[-1],
                'title': info.select_one('h1 .pretty').text,
                'cover': data.select_one('#cover img')['data-src']
            }
            tags = data.select('#tags div:not(.hidden)')
            for j in tags:
                tag_name = list(j.strings)[0].strip('\t\n :').lower()
                if tag_name == 'uploaded':
                    topic[tag_name] = j.find('time')['datetime']
                    continue
                tag_list = j.select('.tags .name')
                if len(tag_list) == 1:
                    topic[tag_name] = tag_list[0].text
                    continue
                topic[tag_name] = []
                for n in tag_list:
                    topic[tag_name].append(n.text)
            self.collection.insert_one(topic)
            sleep(2)

    def get_page(self, page):
        return BeautifulSoup(get(self.url, headers=headers, params={
            'page': page
        }).text, 'lxml').find_all('div', class_='gallery')

    def download(self, root):
        # https://i.nhentai.net/galleries/1815668/1.jpg
        # print(self.collection.find())
        for i in self.collection.find():
            image_id = re.search('(\d+?).+?$', i['cover'])
            path = f"{root}/{image_id}"
            os.makedirs(path, exist_ok=True)
            for j in range(1, int(i['pages']) + 1):
                self.save_image(f"{path}/{j}.jpg", f"https://i.nhentai.net/galleries/{image_id}/{j}.jpg")

    def save_image(self, image_path, url):
        with open(image_path, 'wb') as f:
            f.write(get(url).content)
            print(image_path)
            print(f'成功下载 %s' % url)
            sleep(randint(self.min_time, self.max_time))


if __name__ == '__main__':
    # NHenTai().run()
    current_path = os.getcwd() + '/comic'
    NHenTai().download(current_path)
