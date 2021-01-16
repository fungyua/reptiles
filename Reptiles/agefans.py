from requests import get
from config import headers
from bs4 import BeautifulSoup


class AgeFans:
    def __init__(self):
        self.url = 'https://www.agefans.net'

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_page(self, keyword):
        topics = []
        ls = BeautifulSoup(get(self.url + '/search', headers=headers, params={
            'query': keyword,
            'page': 1
        }).text, 'lxml').select('.blockcontent1>div')
        for i in ls:
            img_el = i.find('img')
            topic = {
                'title': img_el['alt'],
                'img': img_el['src'],
                'url': self.url + i.find('a')['href']
            }
            topics.append(topic)
        BeautifulSoup(get(topics[0]['url'], headers=headers).text, 'lxml').select('.movurl')


if __name__ == '__main__':
    AgeFans().get_page(keyword='鬼灭之刃')
