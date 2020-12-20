import openpyxl
from config.config import mongo, headers
from requests import get
import json


class lagou:
    def __init__(self, word):
        self.url = 'https://www.lagou.com/'
        self.word = word

    def run(self):
        data = json.loads(get(f'{self.url}jobs/list_{self.word}', headers=headers, data={
            'wd': self.word
        }).text)
        print(data)

    def insert(self):
        pass


if __name__ == '__main__':
    lagou(word='python').run()
