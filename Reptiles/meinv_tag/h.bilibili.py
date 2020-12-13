import json
import os
import random
import requests
import time


def get_img(root, image_type, item, args, page, minTime=0, maxTime=1):
    url = 'https://api.vc.bilibili.com/link_draw/v2/'
    for x in range(page):
        data = json.loads(requests.get(f'{url}{image_type}/list?category={item}&{args}&page_num={x}').text)['data']['items']
        for value in data:
            user_name = value['user']['name'].replace("|", "_").replace('.', '_')
            image_name = value['item']['title'].replace("|", "_").replace('.', '_')
            os.makedirs(f'{root}/{image_type}/{item}/{user_name}/{image_name}', 775, True)
            with open(f'{root}/{image_type}/{item}/{user_name}/_{user_name}.jpg', 'wb') as f:
                f.write(requests.get(value['user']['head_url']).content)
                print('成功下载%s的头像' % user_name)
            for o, m in enumerate(value['item']['pictures']):
                print(f'{root}/{image_type}/{item}/{user_name}/{image_name}/{o + 1}.jpg')
                with open(f'{root}/{image_type}/{item}/{user_name}/{image_name}/{o + 1}.jpg', 'wb') as f:
                    f.write(requests.get(m['img_src']).content)
                    print('成功下载%s的第%d张图' % (image_name, o + 1))
                    time.sleep(random.randint(minTime, maxTime))


if __name__ == '__main__':
    category = {'Photo': ['sifu', 'cos'], 'Doc': ['illustration', 'all', 'comic', 'draw']}
    myDir = os.path.split(os.path.realpath(__file__))[0] + '/images'
    get_img(root=myDir, Type='Photo', item='cos', args='type=hot&page_size=20', page=5)
