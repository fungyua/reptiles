import json
import os
import random
import requests
import time


def get_image(image_path, url, min_time, max_time):
    with open(image_path, 'wb') as f:
        f.write(requests.get(url).content)
        print(image_path)
        print(f'成功下载 %s' % url)
        time.sleep(random.randint(min_time, max_time))


def get_img(root, photo_type, item, args, page, min_time=0, max_time=1):
    url = 'https://api.vc.bilibili.com/link_draw/v2/'
    for x in range(page):
        data = json.loads(requests.get(f'{url}{photo_type}/list?category={item}&{args}&page_num={x}').text)['data'][
            'items']
        for value in data:
            user_name = value['user']['name'].replace("|", "_").replace('.', '_')
            image_name = value['item']['title'].replace("|", "_").replace('.', '_')
            image_path = f'{root}/{photo_type}/{item}/{user_name}'
            os.makedirs(f'{image_path}/{image_name}', exist_ok=True)
            get_image(f'{image_path}/_{image_name}.jpg', value['user']['head_url'],
                      min_time, max_time)
            for o, m in enumerate(value['item']['pictures']):
                get_image(f'{image_path}/{image_name}/{o + 1}.jpg', m['img_src'], min_time, max_time)


if __name__ == '__main__':
    category = {'Photo': ['sifu', 'cos'], 'Doc': ['illustration', 'all', 'comic', 'draw']}
    myDir = os.path.split(os.path.realpath(__file__))[0] + '/images'
    get_img(myDir, 'Photo', 'cos', 'type=hot&page_size=20', 5)
