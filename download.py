import wget
import requests
import os

def getdlink(link):
    os.system(r"getdlink_spider.bat " + link)
    dlink, file_type = "", ""
    #解析dlink.json，从一级dlink获取跳转的真实dlink，返回dlink与file_type
    return dlink, file_type

def downloadfile(link, name): #利用wget从真实dlink下载书籍文件，正确命名并存放到bookfiles文件夹
    dlink, file_type = getdlink(link)
    file_name = name + '.' + file_type
    path = './bookfiles/' + file_name
    wget.download(dlink, path)

