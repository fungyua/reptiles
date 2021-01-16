import requests
import random
import time
import os


def save_image(save_dir, headers, url, file_name='only', min_time=0, max_time=1):
    with open(f'{save_dir}/{file_name}{os.path.splitext(url)[1]}', 'wb') as f:
        f.write(requests.get(url, headers=headers).content)
        print(f'成功下载 {url}')
        time.sleep(random.randint(min_time, max_time))

# def get_client():
#     client = MongoClient(
#         "mongodb://%s:%s@%s:%s" % (
#             mongo.get('user'), mongo.get('password'), mongo.get('host'),
#             mongo.get('port')))
#     self.db = self.client[mongo.get('database')]
#     self.collection = self.db[collection_name]
#     if collection_name in self.db.list_collection_names():
#         print('集合已经存在')
#         self.collection.drop()
#         print('集合已经删除')
