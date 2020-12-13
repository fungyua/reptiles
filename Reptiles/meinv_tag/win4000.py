import pymongo
import requests
from lxml import etree
import time
import os
import configparser
import random
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
}

myDir = os.path.split(os.path.realpath(__file__))[0]

def get_taotu_url(collection):
    taotu_infos = []
    if not os.path.exists(f'{myDir}/images'):
        os.mkdir(f'{myDir}/images')
    for i in range(1, 6):
        url = f'http://www.win4000.com/mt/index{i}.html'
        root = etree.HTML(requests.get(url, headers=headers).text)
        ls = root.xpath('/html/body/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a')
        j = 1
        for x in ls:
            data = etree.HTML(requests.get(x.get('href'), headers=headers).text)
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
            if not os.path.exists(f'{myDir}/images/{title}'):
                os.mkdir(f'{myDir}/images/{title}')
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
                    if not os.path.exists(f'{myDir}/images/{title}/{image_name}'):
                        os.mkdir(f'{myDir}/images/{title}/{image_name}')
                    print(max_page)
                    with open(f'{myDir}/images/{title}/{image_name}/1.jpg', 'wb') as f:
                        f.write(requests.get(image_first).content)
                        print(f'成功下载图片：{myDir}/images/{title}/{image_name}/1.jpg')
                    for m in range(2, int(max_page)):
                        image_src = etree.HTML(requests.get(f'http://www.win4000.com/meinv{image_id}_{m}.html').text).xpath(
                            '//*[@class="pic-large"]')[0].get('src')
                        images.append(image_src)
                        print(image_src)
                        with open(f'{myDir}/images/{title}/{image_name}/{m}.jpg', 'wb') as f:
                            f.write(requests.get(image_src).content)
                            print(f'成功下载图片：{myDir}/images/{title}/{image_name}/{m}.jpg')
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
                        if not os.path.exists(f'{myDir}/images/{title}/{image_name}'):
                            os.mkdir(f'{myDir}/images/{title}/{image_name}')
                        print(max_page)
                        with open(f'{myDir}/images/{title}/{image_name}/1.jpg', 'wb') as f:
                            f.write(requests.get(image_first).content)
                            print(f'成功下载图片：{myDir}/images/{title}/{image_name}/1.jpg')
                        for m in range(2, int(max_page)):
                            image_src = etree.HTML(requests.get(f'http://www.win4000.com/meinv{image_id}_{m}.html').text).xpath(
                                '//*[@class="pic-large"]')[0].get('src')
                            images.append(image_src)
                            print(image_src)
                            with open(f'{myDir}/images/{title}/{image_name}/{m}.jpg', 'wb') as f:
                                f.write(requests.get(image_src).content)
                                print(f'成功下载图片：{myDir}/images/{title}/{image_name}/{m}.jpg')
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


def main():
    dbName = 'reptiles'
    collectionName = 'win4000'

    config = configparser.ConfigParser()
    path = myDir + '/../db/config.conf'
    config.read(path)

    client = pymongo.MongoClient(
        "mongodb://%s:%s" % (config.get('mongo', 'dbHost'), config.get('mongo', 'dbPort')))
    db = client[config.get('mongo', 'dbName')]
    collection = db[collectionName]

    if collectionName in client[dbName].list_collection_names():
        print('集合已经存在')
        client[dbName][collectionName].drop()
        print('集合已经删除')

    get_taotu_url(collection)
    print('爬取完毕')


if __name__ == '__main__':
    main()
