import requests
import json
import time


def get_content(self, i):
    params = {
        'type': 'uid',
        'value': self.uid,
        'containerid': 1005055118612601,
        'page': i
    }
    html = requests.get(self.url, headers=self.headers, params=params, timeout=5, verify=False).content.decode('utf-8')
    data = json.loads(html)['data']
    cards = data['cards']
    print(cards)


if __name__ == '__main__':
    get_content(, 1)
