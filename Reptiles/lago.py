from requests import post, get
from selenium import webdriver

# headers = {
#     ':authority': ' www.lagou.com',
#     ':method': 'POST',
#     ':path': '/jobs/positionAjax.json?needAddtionalResult=false',
#     ':scheme': 'https',
#     'accept': 'application/json, text/javascript, */*; q=0.01',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'cache-control': 'no-cache',
#     'content-length': '23',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'cookie': 'JSESSIONID=ABAAABAABAGABFA5A713FD5229C7FF113F9E2401CC9B3DB; WEBTJ-ID=20201219160755-1767a0a7b2e538-0675cd8053b86f-10476177-2073600-1767a0a7b2f19; RECOMMEND_TIP=true; user_trace_token=20201219160756-571479d0-fb14-4cd6-bd07-cdd1c94df728; LGUID=20201219160756-6e8772e1-5340-4f9c-98ff-e44604c54f4d; _ga=GA1.2.1244552721.1608365277; index_location_city=%E5%85%A8%E5%9B%BD; _gat=1; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20201221085902-4bd6b73a-0d9d-4c00-86a7-d8872ee33ceb; PRE_SITE=; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=8c474bd16eefac54163215806103fe30c3144c0f96; LGRID=20201221085922-27460071-c919-44d9-81f1-c4b8c9501bc4; SEARCH_ID=440992e8c0964905887c658d03ee0a08',
#     'origin': 'https://www.lagou.com',
#     'pragma': 'no-cache',
#     'referer': 'https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
#     'x-anit-forge-code': '0',
#     'x-anit-forge-token': 'None',
#     'x-requested-with': 'XMLHttpRequest'
# }


class Lago:
    def __init__(self, word):
        # https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
        self.url = 'https://www.lagou.com/'
        self.word = word

    def run(self):
        pass
        # data = get(f'{self.url}jobs/positionAjax.json', headers=headers, params={
        #     'needAddtionalResult': 'false',
        #     'first': 'true',
        #     'pn': '1',
        #     'kd': 'java'
        # }).text
        # print(data)

    def insert(self):
        pass


if __name__ == '__main__':
    Lago(word='python').run()
