import os
import requests
from fontTools.ttLib import TTFont
from parsel import Selector


def download(urls, rain_num=2):
    print("dowing", urls)
    heads = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58'
    }
    try:
        html = requests.get(urls, headers=heads, verify=True).text
    except Exception as e:
        print("Downing error", e.reason)
        html = None
        if rain_num > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(urls, rain_num - 1)
    return html


def get_num():
    url = 'https://book.qidian.com/info/1011454545'
    body = download(url)
    xbody = Selector(text=body)
    font = get_font(xbody)
    text = xbody.xpath(
        "//div[contains(@class,'book-information')]/div[contains(@class,'book-info')]/p/em[1]/span/text()").extract_first()
    print(jiexi(text, font))


def get_font(xbody):
    path = os.path.dirname(os.path.realpath(__file__))
    font_type = xbody.xpath(
        "//div[contains(@class,'book-information')]/div[contains(@class,'book-info')]/p/em[1]/span/@class").extract_first()
    font_url = "https://qidian.gtimg.com/qd_anti_spider/%s.woff" % font_type
    woff = requests.get(font_url).content
    with open(path + '/fonts.woff', 'wb') as f:
        f.write(woff)
    online_fonts = TTFont(path + '/fonts.woff')
    online_fonts.saveXML("text.xml")
    _dict = online_fonts.getBestCmap()
    return _dict


def jiexi(text, _dict):
    _dic = {
        "six": "6",
        "three": "3",
        "period": ".",
        "eight": "8",
        "zero": "0",
        "five": "5",
        "nine": "9",
        "four": "4",
        "seven": '7',
        "one": "1",
        "two": "2"
    }
    df = r"%s" % text
    df = str(df.split(" "))
    df = df.split("\\U000")
    _df = []
    for i in df:
        i = i.replace("['", "").replace("']", "")
        if i:
            _df.append(int("0x" + i, 16))
    num = list()
    for i in _df:
        _da = _dict.get(i)
        num.append(_dic[_da])
    return "".join(num)


if __name__ == '__main__':
    get_num()