import json
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count

import requests

from config import headers


class hbilibili:
    def __init__(self, root, photo_type, item, args, pages, min_time=0, max_time=1):
        self.root = root
        self.min_time = min_time
        self.max_time = max_time
        self.photo_type = photo_type
        self.item = item
        self.args = args
        with ProcessPoolExecutor(max_workers=cpu_count()) as process:
            process.map(self.run, list(range(pages)))

    def run(self, page):
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_images, json.loads(requests.get(
                f'https://api.vc.bilibili.com/link_draw/v2/{self.photo_type}/list?category={self.item}&{self.args}&page_num={page}',
                headers=headers).text)['data']['items'])

    def get_images(self, data):
        user_name = data['user']['name'].replace("|", "_").replace('.', '_')
        image_name = data['item']['title'].replace("|", "_").replace('.', '_')
        image_path = f'{self.root}/{self.photo_type}/{self.item}/{user_name}'
        os.makedirs(f'{image_path}/{image_name}', exist_ok=True)
        self.save_image(f'{image_path}/_avatar.jpg', data['user']['head_url'])
        for o, m in enumerate(data['item']['pictures']):
            self.save_image(f'{image_path}/{image_name}/{o + 1}.jpg', m['img_src'])

    def save_image(self, image_path, url):
        with open(image_path, 'wb') as f:
            f.write(requests.get(url).content)
            print(image_path)
            print(f'成功下载 %s' % url)
            time.sleep(random.randint(self.min_time, self.max_time))


if __name__ == '__main__':
    category = {'Photo': ['sifu', 'cos'], 'Doc': ['illustration', 'all', 'comic', 'draw']}
    myDir = os.path.split(os.path.realpath(__file__))[0] + '/images'
    hbilibili(myDir, 'Photo', 'cos', 'type=hot&page_size=20', 5)
