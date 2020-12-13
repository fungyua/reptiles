import os
import json
import time
import random
import requests
from multiprocessing import Process, Queue, Pool, Lock


class pixivic(Process):
    def __init__(self, root, url, params, min_time=0, max_time=1):
        Process.__init__(self)
        self.headers = {
            'referer': 'https://www.pixiv.net/'
        }
        self.root = root
        self.url = url
        self.params = params
        self.min_time = min_time
        self.max_time = max_time
        self.data = json.loads(requests.get(self.url, self.params).text)['data']
        self.newData = {}

    def get_image(self, image_path, url, min_time, max_time):
        with open(image_path, 'wb') as f:
            f.write(requests.get(url, headers=self.headers).content)
            print(image_path)
            print(f'成功下载 {url}')
            time.sleep(random.randint(min_time, max_time))

    def run(self):
        for k, v in enumerate(self.data):
            image_path = f'{self.root}/{v["type"]}/{v["title"]}'
            os.makedirs(image_path, exist_ok=True)
            avatar = v['artistPreView']['avatar']
            self.get_image(f'{image_path}/_avatar{os.path.splitext(avatar)[1]}', avatar, self.min_time, self.max_time)
            for n, m in enumerate(v['imageUrls']):
                url = m['original']
                self.get_image(f'{image_path}/{n + 1}{os.path.splitext(url)[1]}', url, self.min_time,
                               self.max_time)


if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0] + '/images'
    # threadList = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    # Pool(processes=20, initializer=)
    # for i in range(4):
    #     p = pixivic(root=current_path, url='https://pix.ipv4.host/ranks',
    #                 params={'page': 1, 'date': '2020-12-10', 'mode': 'day', 'pageSize': 200})

    pixivic(root=current_path, url='https://pix.ipv4.host/ranks',
            params={'page': 1, 'date': '2020-12-10', 'mode': 'day', 'pageSize': 200})
