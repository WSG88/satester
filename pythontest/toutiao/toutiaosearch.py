# -*- coding: utf8 -*-

import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf8')
import json

import requests

# print '打印所有汉字'
# def print_unicode(start, end):
#     Start = start
#     while Start <= end:
#         ustr = '\u' + hex(Start)[2:]
#         index = Start - start + 1
#         print str(index) + '\t' + ustr.decode('unicode-escape')
#         Start = Start + 1
# print_unicode(0x4e00, 0x9fbf)

key = "桥梁施工"
key = "高铁施工工艺"
print key
key = urllib.quote(key)
print key
url = 'http://www.toutiao.com/search_content/?offset=0&format=json&keyword=' + key + '&autoload=true&count=20&cur_tab=1'
print url
print ''
print ''
print ''

wbdata = requests.get(url).text

data = json.loads(wbdata)
news = data['data']

for n in news:
    print ''
    if 'title' in n:
        title = n['title']
        print(title)
    if 'source' in n:
        source = n['source']
        print(source)
    if 'keywords' in n:
        keywords = n['keywords']
        print(keywords)
    if 'article_url' in n:
        article_url = n['article_url']
        print(article_url)
