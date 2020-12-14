import os
import json
import time
import random
import requests
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count


class pixivic:
    image_path = ''

    def __init__(self, root, url, params, min_time=0, max_time=1):
        # ProcessPoolExecutor.__init__(self)
        # super(pixivic, self).__init__()
        self.headers = {
            'referer': 'https://www.pixiv.net/'
        }
        self.root = root
        self.params = params
        self.min_time = min_time
        self.max_time = max_time
        self.data = json.loads(requests.get(url, self.params).text)['data']

    def save_image(self, image_path, url, min_time, max_time):
        with open(image_path, 'wb') as f:
            f.write(requests.get(url, headers=self.headers).content)
            print(image_path)
            print(f'成功下载 {url}')
            time.sleep(random.randint(min_time, max_time))

    def get_list(self, data):
        self.image_path = f'{self.root}/{data["type"]}/{data["title"]}'
        os.makedirs(self.image_path, exist_ok=True)
        avatar = data['artistPreView']['avatar']
        self.save_image(f'{self.image_path}/_avatar{os.path.splitext(avatar)[1]}', avatar, self.min_time, self.max_time)
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_images, p.data)

    def get_images(self, data, ):
        for key, val in enumerate(data['imageUrls']):
            url = val['original']
            self.save_image(f'{self.image_path}/{key + 1}{os.path.splitext(url)[1]}', url, self.min_time,
                            self.max_time)


if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0] + '/images'
    # threadList = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    p = pixivic(root=current_path, url='https://pix.ipv4.host/ranks',
                params={'page': 1, 'date': '2020-12-12', 'mode': 'day', 'pageSize': 200})
    # print(p.data)
    with ProcessPoolExecutor(max_workers=cpu_count()) as t:
        pool_out_puts = t.map(p.get_list, p.data)
