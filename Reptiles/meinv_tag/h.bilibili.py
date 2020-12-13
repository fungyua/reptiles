import json
import os
import random
import requests
import time


def get_img(root, Type, item, args, page, minTime=0, maxTime=1):
    url = 'https://api.vc.bilibili.com/link_draw/v2/'
    for x in range(page):
        data = json.loads(requests.get(f'{url}{Type}/list?category={item}&{args}&page_num={x}').text)['data']['items']
        for value in data:
            userName = value['user']['name'].replace("|", "_").replace('.', '_')
            imageName = value['item']['title'].replace("|", "_").replace('.', '_')
            os.makedirs(f'{root}/{Type}/{item}/{userName}/{imageName}', 775, True)
            with open(f'{root}/{Type}/{item}/{userName}/_{userName}.jpg', 'wb') as f:
                f.write(requests.get(value['user']['head_url']).content)
                print('成功下载%s的头像' % userName)
            for o, m in enumerate(value['item']['pictures']):
                print(f'{root}/{Type}/{item}/{userName}/{imageName}/{o + 1}.jpg')
                with open(f'{root}/{Type}/{item}/{userName}/{imageName}/{o + 1}.jpg', 'wb') as f:
                    f.write(requests.get(m['img_src']).content)
                    print('成功下载%s的第%d张图' % (imageName, o + 1))
                    time.sleep(random.randint(minTime, maxTime))


if __name__ == '__main__':
    category = {'Photo': ['sifu', 'cos'], 'Doc': ['illustration', 'all', 'comic', 'draw']}
    myDir = os.path.split(os.path.realpath(__file__))[0] + '/images'
    get_img(root=myDir, Type='Photo', item='cos', args='type=hot&page_size=20', page=5)
