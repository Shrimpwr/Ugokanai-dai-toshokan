import sys
import os
from typing import Hashable
from PyQt5.QtWidgets import QApplication, QMainWindow
import download
import json
import books_manage as manage
import Ui_untitled

def __init__(): # 程序初始化
    root = manage.treenode(True, {"title":"root"}, [])
    with open("./data/booklist.json", "r", encoding='utf-8') as f: 
        filestr = f.read()
        if len(filestr): root.read_file(filestr)
    hashtable = manage.hash()
    hashtable.insert(root)
    hashtable.create_hashtable(root)
    return root, hashtable

def __finish__(): # 程序退出，导出booklist文件
    with open("./data/booklist.json", "w", encoding='utf-8') as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))

def addbook(dir): # 向目录中添加书籍
    with open("./data/search_results.json", "r", encoding='utf-8') as f:
        results = json.load(f)
        for book in results:
            if hashtable.search(book["title"]) != -1:
                continue
            # 检索哈希表，若本地书库中已有同名书籍，则不添加
            newnode = manage.treenode(False, book, [])
            dir.insert(newnode)
            hashtable.insert(newnode)

def downloadbook(book):
    file_type = download.downloadfile(book.info["link"], book.info["title"])
    book.info["file_type"] = file_type

def delbook(book):
    dir = book.father
    os.remove("./bookfiles/" + book.info["title"].replace(": ", "：") + "." + book.info["file_type"])
    dir.remove(book)

def search_online(keyword): # 运行在线搜索爬虫
    os.system(r"search_spider.bat " + keyword)
    
if __name__ == '__main__':
    root, hashtable = __init__()
    # search_online("python")
    # addbook(root)
    # root.sort("title")
    downloadbook(root.sons[0])
    temp = hashtable.search("Introduction to Machine Learning with Python: A Guide for Data Scientists")
    print(temp.info["authors"])
    # delbook(root.sons[0])
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
    __finish__()