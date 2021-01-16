import logging
import re
import threading

import config
from crawler.crawler_thread import CrawlerThread
from crawler.item import Item
from crawler.utils.storage import Storage

logger = logging.getLogger("crawler")
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)


class Crawler:

    @classmethod
    def check(cls, url):
        item = parse_url(url)

        result = {}
        if item:
            result['item'] = item
        else:
            result['data'] = {
                "code": 400,
                "status": "error",
                "message": "url is not support."
            }
            return result

        storage = Storage(item.domain, item.id)
        result['path'] = storage.get_comic_file_path()
        if storage.check_comic():
            result['data'] = {
                "code": 200,
                "status": "ready",
                "message": "files has generated.",
                "url": storage.get_comic_public_download_url()
            }
            return result

        thread = get_thread(get_thread_name(item))
        if thread:
            result['item'] = thread.item
            result['data'] = {
                "code": 202,
                "status": "generating",
                "progress": thread.progress
            }
            return result
        else:
            result['data'] = {
                "code": 404,
                "status": "absent",
                "message": "not crawled yet",
            }
            return result

    @classmethod
    def crawl(cls, url):
        result = cls.check(url)
        if result['data']['code'] != 404:
            return result

        item = result['item']
        result.clear()

        thread = CrawlerThread(name=get_thread_name(item), item=item, url=url)
        if thread:
            thread.start()
            result['item'] = thread.item
            result['data'] = {
                "code": 201,
                "status": "started",
                "message": "crawler thread started."
            }
            return result
        else:
            result['data'] = {
                "code": 401,
                "status": "error",
                "message": "create crawler thread failed."
            }
            return result


def parse_url(url):
    match = re.search(r'nhentai\.net/g/(\d+)', url)
    item = Item()
    if match:
        item.id = match.group(1)
        item.domain = config.DOMAIN.nhentai_net
    match = re.search(r'wnacg\.org\/photos-index-aid-([0-9]+)\.html$', url)
    if match:
        item.id = match.group(1)
        item.domain = config.DOMAIN.wnacg_org
    match = re.search(r'e-hentai\.org/g/(\d+)/(\w+)', url)
    if match:
        item.id = match.group(1)
        item.token = match.group(2)
        item.domain = config.DOMAIN.ehentai_org

    if item.id:
        return item
    else:
        return None


def get_thread_name(item):
    return "CrawlerThread." + item.domain.value + "@" + item.id


def get_thread(thread_name):
    for t in threading.enumerate():
        if t.name == thread_name:
            return t
    return None
