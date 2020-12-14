import os
import json
import time
import random
import requests
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

start = time.time()


class pixiv:
    image_path = ''

    def __init__(self, root, min_time=0, max_time=1):
        self.headers = {
            'referer': 'https://www.pixiv.net/'
        }
        self.root = root
        self.min_time = min_time
        self.max_time = max_time

    def get_list(self, data):
        self.image_path = f'{self.root}/{data["type"]}/{data["title"]}'
        os.makedirs(self.image_path, exist_ok=True)
        self.save_image(data['artistPreView']['avatar'], '_avatar')
        with ThreadPoolExecutor(max_workers=cpu_count()) as thread:
            thread.map(self.get_images, data['imageUrls'])

    def get_images(self, data):
        if len(data) == 1:
            self.save_image(data[0]['original'])
        else:
            for key, val in enumerate(data):
                print(key, val)
                self.save_image(val['original'], str(key + 1))

    def save_image(self, url, file_name='only'):
        with open(f'{self.image_path}/{file_name}{os.path.splitext(url)[1]}', 'wb') as f:
            f.write(requests.get(url, headers=self.headers).content)
            print(f'成功下载 {url}')
            time.sleep(random.randint(self.min_time, self.max_time))


if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0] + '/images'
    all_data = json.loads(requests.get('https://pix.ipv4.host/ranks',
                                       {'page': 1, 'date': '2020-12-12', 'mode': 'day', 'pageSize': 5}).text)['data']
    # print(p.data)
    with ProcessPoolExecutor(max_workers=cpu_count()) as t:
        pool_out_puts = t.map(pixiv(current_path).get_list, all_data)
    end = time.time()
    print(f'耗时：{end - start}s')
