from bs4 import BeautifulSoup as Bs
from requests import get
from config import headers, aria2
from aria2_rpc import Aria2RPC


class OHentai:
    def __init__(self):
        self.url = 'https://ohentai.org'
        self.aria2 = Aria2RPC(aria2.get('host'), aria2.get('port'), aria2.get('token'))

    def get_page(self):
        source = Bs(get(self.url, headers=headers).text, 'lxml').select('.videobrickwrap .videobrick')
        for i in source:
            if not i.find(class_='adtag'):
                print(i.find(class_='videotitle').text)

    def get_cord(self):
        pass


if __name__ == '__main__':
    OHentai().get_page()
