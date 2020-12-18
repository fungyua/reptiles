import os
import random
import re
import time

import pymongo
import requests
from lxml import etree
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from config.config import mongo

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 '
}


class win4000:
    def __init__(self, root, url, page, db_config, min_time=0, max_time=1):
        self.root = root
        self.min_time = min_time
        self.max_time = max_time
        self.data = requests.get(url, )
        collection_name = 'win4000'
        client = pymongo.MongoClient(
            "mongodb://%s:%s@%s:%s" % (
                db_config.get('user'), db_config.get('password'), db_config.get('host'),
                db_config.get('port')))
        self.db = client.get(db_config.get('database'))
        self.collection = self.db.get(collection_name)
        if collection_name in self.db.list_collection_names():
            print('集合已经存在')
            self.collection.drop()
            print('集合已经删除')

    def run(self):
        taotu_infos = []
        if not os.path.exists(f'{self.root}'):
            os.mkdir(f'{self.root}')
        root = etree.HTML(requests.get(url=f'{url}{page}.html', headers=headers).text)
        ls = root.xpath('/html/body/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a/@href')
        for x in ls:
            print(x)
            time.sleep(random.randint(self.min_time, self.max_time))
            print(self.collection.find_one())
        j = 1
        for x in ls:
            data = etree.HTML(requests.get(x, headers=headers).text)
            title = x.xpath('./p')[0].text[0: -4]
            taotu_info = {
                '_id': j,
                'title': title,
                'url': x.get('href'),
                'list': [],
                'desc': data.xpath('/html/body/div[4]/div/div[2]/div/div[1]/p')[0].text
            }
            j = j + 1
            print('正在爬取 %s 的图片' % title)
            if not os.path.exists(f'{my_dir}/images/{title}'):
                os.mkdir(f'{my_dir}/images/{title}')
            urls = data.xpath('/html/body/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a')
            page_url = data.xpath('/html/body/div[4]/div/div[3]/div[1]/div[2]/div/a[@class="num"]')
            while True:
                for y in urls:
                    image_url = y.get('href')
                    image_id = re.findall(r'(?<=[a-zA-Z])\d+?$', image_url[:-5])[0]
                    image = etree.HTML(requests.get(image_url, headers=headers).text)
                    image_first = image.xpath('//*[@class="pic-large"]')[0].get('src')
                    images = [image_first]
                    max_page = image.xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/em/text()')[0]
                    image_name = image.xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/h1')[0].text
                    if not os.path.exists(f'{my_dir}/images/{title}/{image_name}'):
                        os.mkdir(f'{my_dir}/images/{title}/{image_name}')
                    print(max_page)
                    with open(f'{my_dir}/images/{title}/{image_name}/1.jpg', 'wb') as f:
                        f.write(requests.get(image_first).content)
                        print(f'成功下载图片：{my_dir}/images/{title}/{image_name}/1.jpg')
                    for m in range(2, int(max_page)):
                        image_src = \
                            etree.HTML(requests.get(f'http://www.win4000.com/meinv{image_id}_{m}.html').text).xpath(
                                '//*[@class="pic-large"]')[0].get('src')
                        images.append(image_src)
                        print(image_src)
                        with open(f'{my_dir}/images/{title}/{image_name}/{m}.jpg', 'wb') as f:
                            f.write(requests.get(image_src).content)
                            print(f'成功下载图片：{my_dir}/images/{title}/{image_name}/{m}.jpg')
                    taotu_info['list'].append({
                        'title': image_name,
                        'images': images
                    })

                    taotu_infos.append(taotu_info)
                if not page_url:
                    break
                for n in page_url:
                    for y in etree.HTML(requests.get(n.get('href'), headers=headers).text).xpath(
                            '/html/body/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a'):
                        image_url = y.get('href')
                        image_id = re.findall(r'(?<=[a-zA-Z])\d+?$', image_url[:-5])[0]
                        image = etree.HTML(requests.get(image_url, headers=headers).text)
                        image_first = image.xpath('//*[@class="pic-large"]')[0].get('src')
                        images = [image_first]
                        max_page = image.xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/em/text()')[0]
                        image_name = image.xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/h1')[0].text
                        if not os.path.exists(f'{my_dir}/images/{title}/{image_name}'):
                            os.mkdir(f'{my_dir}/images/{title}/{image_name}')
                        print(max_page)
                        with open(f'{my_dir}/images/{title}/{image_name}/1.jpg', 'wb') as f:
                            f.write(requests.get(image_first).content)
                            print(f'成功下载图片：{my_dir}/images/{title}/{image_name}/1.jpg')
                        for m in range(2, int(max_page)):
                            image_src = \
                                etree.HTML(requests.get(f'http://www.win4000.com/meinv{image_id}_{m}.html').text).xpath(
                                    '//*[@class="pic-large"]')[0].get('src')
                            images.append(image_src)
                            print(image_src)
                            with open(f'{my_dir}/images/{title}/{image_name}/{m}.jpg', 'wb') as f:
                                f.write(requests.get(image_src).content)
                                print(f'成功下载图片：{my_dir}/images/{title}/{image_name}/{m}.jpg')
                        taotu_info['list'].append({
                            'title': image.xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/h1')[0].text,
                            'images': images
                        })
                        taotu_infos.append(taotu_info)
                        time.sleep(random.randint(1, 3))
                break
            collection.insert_one(taotu_info)
            print('%s 已插入数据库' % title)
        # return taotu_infos

    def get_image(self, image_path, url):
        with open(image_path, 'wb') as f:
            f.write(requests.get(url).content)
            print(image_path)
            time.sleep(random.randint(self.min_time, self.max_time))


if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0]
    my_dir = current_path + '/../images/dongman'
    # win4000(my_dir, 'http://www.win4000.com/mt/index', 1, config['mongo']).run()
    # print('爬取完毕')
