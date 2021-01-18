import base64
import json
import time

import requests
from bs4 import BeautifulSoup as Bs

from settings import request_headers, aria2url, aria2token, proxies


def get_page(page_address, headers=None, cookie=None):
    if headers is None:
        headers = {}
    pic_page = None
    inner_head = request_headers.copy()
    inner_head.update(headers)
    try:
        pic_page = requests.get(page_address, headers=inner_head, proxies=proxies, cookie=cookie)
    except Exception as e:
        return None
    if not pic_page:
        return None
    pic_page.encoding = 'utf-8'
    text_response = pic_page.text
    content = Bs(text_response, 'lxml')

    return content


def pos_torrent(path, dir):
    with open(path, 'rb') as f:
        b64str = str(base64.b64encode(f.read()), 'utf-8')
    url = aria2url
    id_str = "AriaNg_%s_0.043716476479668254" % str(int(time.time()))
    req = requests.post(url, data=json.dumps({"jsonrpc": "2.0", "method": "aria2.addTorrent",
                                              "id": str(base64.b64encode(id_str.encode('utf-8')), 'utf-8').strip('='),
                                              "params": ["token:" + aria2token, b64str, [],
                                                         {'dir': dir, 'allow-overwrite': "true"}]}))
    if req.status_code == 200:
        return req.json().get('result')
    else:
        return False


def download_img(page_address, filepath, cookie=None):
    try:
        pic_page = requests.get(page_address, headers=request_headers, proxies=proxies, cookies=cookie, timeout=8)
        if pic_page.status_code == 200:
            pic_content = pic_page.content
            with open(filepath, 'wb') as file:
                file.write(pic_content)
        return pic_page.status_code
    except Exception as e:
        return e
