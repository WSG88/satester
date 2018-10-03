# coding:utf-8  fxb_qzyx@163.com


import re
import time
from threading import Thread

import requests
from lxml import etree
from queue import Queue

base_url = "https://www.zhipin.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

jobs_queue = Queue()

url_queue = Queue()

regx_obj = re.compile(r'<br/>|<(em).*?>.*?</\1>')

import json


def save_file(name, item):
    fileObject = open(name, 'a+')
    a = fileObject.read()
    if len(a) == 0:
        fileObject.write("[")
    jsObj = json.dumps(item)
    fileObject.write(jsObj)
    fileObject.write(",")
    fileObject.close()


def send_request(url_path, headers, param=None):
    """
    :brief 发送请求，获取html响应(这里是get请求)
    :param url_path: url地址
    :param headers: 请求头参数
    :param param: 查询参数, 如：param = {'query': 'python', 'page': 1}
    :return: 返回响应内容
    """
    response = requests.get(url=url_path, params=param, headers=headers)

    response = regx_obj.sub('', response.text)

    return response


def parse_data():
    try:
        while True:
            detail_url = url_queue.get(timeout=25)

            html = send_request(detail_url, headers, param=None)
            html_obj = etree.HTML(html)
            item = {}

            # 发布日期
            item['publishTime'] = html_obj.xpath(".//div[@class='info-primary']//span[@class='time']/text()")[0].strip(
                '\n')
            # 职位名
            item['position'] = html_obj.xpath(".//div[@class='info-primary']//h1/text()")[0].strip('\n')
            # 发布者姓名
            item['publisherName'] = html_obj.xpath("//div[@class='job-detail']//h2/text()")[0].strip('\n')
            # 发布者职位
            item['publisherPosition'] = html_obj.xpath("//div[@class='detail-op']//p/text()")[0].strip('\n')
            # 薪水
            item['salary'] = html_obj.xpath(".//div[@class='info-primary']//span[@class='badge']/text()")[0].strip('\n')
            # 公司名称
            item['companyName'] = html_obj.xpath("//div[@class='info-company']//h3/a/text()")[0].strip('\n')
            # 公司类型
            item['companyType'] = html_obj.xpath("//div[@class='info-company']//p//a/text()")[0].strip('\n')
            # 公司规模
            item['companySize'] = html_obj.xpath("//div[@class='info-company']//p/text()")[0].strip('\n')
            # 工作职责
            item['responsibility'] = html_obj.xpath("//div[@class='job-sec']//div[@class='text']/text()")[0].strip()
            # 招聘要求
            item['requirement'] = html_obj.xpath("//div[@class='job-banner']//div[@class='info-primary']//p/text()")[
                0].strip('\n')
            print(item)
            jobs_queue.put(item)  # 添加到队列中
            save_file("item.json", item)  # 保存到文件
            time.sleep(15)
    except:
        pass


def detail_url(param):
    # 上海
    city_url = '/'.join([base_url, "c101020100-p100301/"])
    print (city_url)

    html = send_request(city_url, headers, param=param)
    # 列表页页面
    html_obj = etree.HTML(html)
    # 提取详情页url地址
    nodes = html_obj.xpath(".//div[@class='info-primary']//a/@href")
    for node in nodes:
        detail_url = '/'.join([base_url, node])  # 拼接成完整的url地址
        print(detail_url)
        url_queue.put(detail_url)  # 添加到队列中


def start_work(page):
    for page in range(page, page + 1):
        param = {'query': '测试', 'page': page}
        producter = Thread(target=detail_url, args=[param])
        producter.start()

    for i in range(1):
        consumer = Thread(target=parse_data)
        consumer.start()


if __name__ == "__main__":
    pages = int(input('请输入需要爬取的页面数：[1-10]:'))
    for page in range(1, pages + 1):
        start_work(page)
time.sleep(15)
