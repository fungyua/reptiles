import configparser
import os
import pymongo
import requests
from lxml import etree


def main():
    html = etree.HTML(requests.get(url, headers).content.decode('utf-8'))
    ls = html.xpath('/html/body/div[4]/div[1]/div/div[2]/ul[1]/li/a')
    topics = []
    i = 1
    for target in ls:
        topic = {
            '_id': i,
            'title': target.xpath('.//i')[0].text,
            'url': target.get('href'),
            'time': target.xpath('.//em')[0].text,
            'image': target.get('rel')
        }
        topics.append(topic)
        i = i + 1
    return topics


if __name__ == '__main__':
    url = 'https://www.lssdjt.com/'
    collectionName = 'today'
    drive = 'mongo'

    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/db/config.conf'
    config.read(path)

    client = pymongo.MongoClient(
        "mongodb://%s:%s@%s:%s" % (
            config.get(drive, 'user'), config.get(drive, 'password'), config.get(drive, 'host'),
            config.get(drive, 'port')))
    db = client[config.get(drive, 'database')]
    collection = db[collectionName]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 '
    }
    if collectionName in db.list_collection_names():
        print('集合已经存在')
        db[collectionName].drop()
        print('集合已经删除')
    collection.insert_many(main())
    print('爬取完毕')
