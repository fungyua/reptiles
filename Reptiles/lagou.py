from selenium import webdriver
import pyquery as pq
import time
import os


class LaGou:
    def __init__(self):
        self.path = os.getcwd()
        self.drive = webdriver.Chrome(executable_path=self.path + '/chromedriver')
        self.drive.implicitly_wait(5)
        # https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=
        self.url = 'https://www.lagou.com/'
        self.data = []
        self.drive.get(self.url + '/jobs/list_python?labelWords=&fromSearch=true&suginput=')

    def run(self):
        while True:
            page = self.drive.find_element_by_css_selector(".pager_next ").get_attribute('class')
            if page == 'pager_next ':
                items = pq.PyQuery(self.drive.page_source).find('.con_list_item')
                print('items', items)
                time.sleep(2)
            else:
                break

    def get_data(self, page):
        pass


if __name__ == '__main__':
    LaGou().run()
