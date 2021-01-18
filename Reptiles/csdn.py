import json
from datetime import datetime

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from requests import post

from config import headers


def crawl_data() -> dict:
    url = 'https://bss.csdn.net/m/topic/blog_star2020/getUsers'
    data = {
        'number': ''
    }
    response = post(url=url, headers=headers, data=data)
    response_json = json.loads(response.text)
    return response_json


def data_processing(data) -> list:
    all_data = []
    csdn_data = data['data']
    for csdn in csdn_data:
        vote_num = int(csdn['vote_num'])  # 票数
        number = csdn['number']  # 编号
        csdn_id = csdn['title']  # CSDN ID
        nick_name = csdn['nick_name']  # 昵称
        code_level = csdn['codeLevel']  # 码龄
        article_count = csdn['article_count']  # 文章数
        csdn_url = 'https://blog.csdn.net/' + csdn_id  # 主页
        url = csdn['url']  # 投票地址
        # avatar = c['avatar']                             # 头像地址
        personal_information = [vote_num, number, csdn_id, nick_name, code_level, article_count, csdn_url, url]
        all_data.append(personal_information)
    # 按照票数排序
    all_data_sorted = sorted(all_data, key=lambda x: x[0], reverse=True)
    # 添加排名
    rank = 1
    for a in all_data_sorted:
        a.insert(0, rank)
        rank += 1
    # print(all_data_sorted)
    return all_data_sorted


def create_table(data, crawl_time):
    table = Table(page_title="TRHX丨CSDN 2020 博客之星实时数据")
    header = ["排名", "票数", "编号", "CSDN ID", "CSDN 昵称", "码龄", "文章数", "主页", "投票地址"]
    rows = data
    table.add(header, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(
            title="CSDN 2020 博客之星实时数据排名（每10分钟更新一次）",
            subtitle='上次更新时间：' + str(
                crawl_time) + '&nbsp;&nbsp;&nbsp;&nbsp;数据来源：https://bss.csdn.net/m/topic/blog_star2020' + "\n\n作者：TRHX • 鲍勃&nbsp;&nbsp;&nbsp;&nbsp;为作者投上一票吧：https://bss.csdn.net/m/topic/blog_star2020/detail?username=qq_36759224",
            title_style={"style": "font-size:20px; font-weight:bold; text-align: center"},
            subtitle_style={"style": "font-size:15px; text-align: center"})
    )
    table.render("csdn_blog_star_2020.html")


if __name__ == '__main__':
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data = crawl_data()
    data_sorted = data_processing(json_data)
    create_table(data_sorted, time_now)
