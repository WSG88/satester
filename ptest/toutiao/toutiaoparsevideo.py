# -*- coding: utf8 -*-

# http://www.jianshu.com/p/3559ad586c98
import test_json

import requests

# from pyquery import PyQuery as pq
#
# r = requests.get('http://www.toutiao.com/a6296462662335201793/')
# d = pq(r.content)
# print d
# print type(d)
# vid = d('#video').attr('tt-videoid')
# print vid

r = requests.get('http://www.toutiao.com/a6296462662335201793/')
s = r.content
# print s
vid = s[s.rfind("videoid:'") + len("videoid:'"):s.rfind("share_url:'")]
print vid
vid = vid.strip().lstrip().rstrip(',')[:-1]
print vid

import random

r = str(random.random())[2:]

import urlparse
import binascii


def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n


url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % vid
n = urlparse.urlparse(url).path + '?r=' + r

c = binascii.crc32(n)
s = right_shift(c, 0)

print url + '?r=%s&s=%s' % (r, s)
re = requests.get(url + '?r=%s&s=%s' % (r, s))
rj = re.json()
print rj

print(test_json.dumps(rj, indent=1))

import base64

main_url = "aHR0cDovL3YzLXR0Lml4aWd1YS5jb20vOGIwYTFiY2E4ZjM0NDJkM2MyYjdkYjhkZjJmOTExZDcvNTljYjJjYzEvdmlkZW8vbS8yMjAzNDMwNzcxZjMyNmY0ZDUxOTRiNTYyMzdhNmEyMzFmYzExNDI1MmIwMDAwMGIzNmI5NmE0N2EwLw=="
print base64.standard_b64decode(main_url)
