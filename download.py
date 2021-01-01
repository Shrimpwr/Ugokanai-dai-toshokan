import wget
import requests
import os
import json

def get_real_address(url):
    HEADERS = {
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    return res.headers['Location'] if res.status_code == 302 else None

def getdlink(link):
    os.system(r"getdlink_spider.bat " + link)
    with open('./data/dlink.json', 'r') as f: data = json.load(f)[0]
    dlink, file_type = data.values()
    dlink = get_real_address(dlink)
    return dlink, file_type

def downloadfile(link, name): #利用wget从真实dlink下载书籍文件，正确命名并存放到bookfiles文件夹
    dlink, file_type = getdlink(link)
    file_name = name + '.' + file_type
    path = './bookfiles/' + file_name
    wget.download(dlink, path)

downloadfile("https://zh.1lib.us/book/3641986/812370", "Python Basics")
