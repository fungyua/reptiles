import json
import os
import random
import time

from aria2_rpc import Aria2RPC
from requests import get

from config import headers, aria2

import pretty_errors


class HBiliBili:
    def __init__(self, root, photo_type, item, args, page, min_time=0, max_time=1):
        self.root = root
        self.min_time = min_time
        self.max_time = max_time
        self.photo_type = photo_type
        self.item = item
        self.args = args
        self.aria2 = Aria2RPC(host=aria2.get('host'), port=aria2.get('port'), token=aria2.get('token'))
        self.run(page)

    def run(self, page):
        for i in json.loads(get(
                f'https://api.vc.bilibili.com/link_draw/v2/{self.photo_type}/list?category={self.item}&{self.args}&page_num={page}',
                headers=headers).text)['data']['items']:
            self.get_images(i)

    def get_images(self, data):
        user_name = data['user']['name'].replace("|", "_").replace('.', '_')
        image_name = data['item']['title'].replace("|", "_").replace('.', '_')
        image_path = f'{self.root}/{self.photo_type}/{self.item}/{user_name}'
        dl_path = f'{image_path}/{image_name}'
        os.makedirs(dl_path, exist_ok=True)
        print(image_path + '/_avatar.jpg', end='  ')
        print(os.path.isfile(image_path + '/_avatar.jpg'))
        if not os.path.isfile(image_path + '/_avatar.jpg'):
            self.aria2.addUri([data['user']['head_url']], {
                'dir': image_path,
                'out': '_avatar.jpg'
            })
        for o, m in enumerate(data['item']['pictures']):
            self.aria2.addUri([m['img_src']], {
                'dir': dl_path,
                'out': f'{o + 1}.jpg'
            })
        time.sleep(random.randint(self.min_time, self.max_time))

    def save_image(self, image_path, url):
        with open(image_path, 'wb') as f:
            f.write(get(url).content)
            print(image_path)
            print(f'成功下载 %s' % url)
            time.sleep(random.randint(self.min_time, self.max_time))


if __name__ == '__main__':
    category = {'Photo': ['sifu', 'cos'], 'Doc': ['illustration', 'all', 'comic', 'draw']}
    myDir = os.getcwd() + '/images'
    HBiliBili(myDir, 'Photo', 'cos', 'type=hot&page_size=20', 0, 2, 4)
