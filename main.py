import sys
import os
from typing import Hashable
from PyQt5.QtWidgets import QApplication, QMainWindow
import download
import json
import books_manage as manage
from UI.stacklayout import MainWidget

from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget

# 导入生成的 ui
from UI.Ui_main import Ui_Form
from UI.Ui_book_page import Ui_book_page
from UI.Ui_search_page import Ui_search_page
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class FrameBookPage(QWidget, Ui_book_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class FrameSearchPage(QWidget, Ui_search_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MainWidget(QWidget, Ui_Form):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 实例化一个堆叠布局
        self.qsl = QStackedLayout(self.frame)
        # 实例化分页面
        self.book = FrameBookPage()
        self.search = FrameSearchPage()
        # 加入到布局中
        self.qsl.addWidget(self.book)
        self.qsl.addWidget(self.search)
        # 控制函数
        self.controller()

    def controller(self):
        self.btn_manage.clicked.connect(self.switch)
        self.btn_search.clicked.connect(self.switch)
        self.search.pushButton.clicked.connect(self.start_search) # 进行搜索

    def switch(self):
        sender = self.sender().objectName()

        index = {
            "btn_manage": 0,
            "btn_search": 1,
        }

        self.qsl.setCurrentIndex(index[sender])
    
    def start_search(self):
        keyword = self.search.lineEdit.text()
        search_online(keyword)

def __init__(): # 程序初始化
    if not os.path.exists("./data/booklist.json"):
        f = open("./data/booklist.json", "wb")
        f.close()

    root = manage.treenode(True, {"title":"root"}, [])
    with open("./data/booklist.json", "r", encoding='utf-8') as f: 
        filestr = f.read()
        if len(filestr): root.read_file(filestr)

    hashtable = manage.hash()
    hashtable.insert(root)
    hashtable.create_table(root)
    return root, hashtable

def __finish__(): # 程序退出，导出booklist文件
    with open("./data/booklist.json", "w", encoding='utf-8') as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))

def add_book(dir): # 向目录中添加书籍
    with open("./data/search_results.json", "r", encoding='utf-8') as f:
        results = json.load(f)
        for book in results:
            if hashtable.search(book["title"]) != -1: # 检索哈希表，若本地书库中已有同名书籍，则不添加
                continue
            newbook = manage.treenode(False, book, [])
            dir.insert(newbook)
            hashtable.insert(newbook)

def add_dir(father_dir, title):
    temp = hashtable.search(title)
    if temp != -1 and temp in father_dir.sons: # 同一个上级目录下不允许存在两个同名文件夹
        return -1  
    newdir = manage.treenode(True, {"title":title}, [])
    father_dir.insert(newdir)
    hashtable.insert(newdir)
        
def download_book(book):
    file_type = download.downloadfile(book.info["link"], book.info["title"])
    book.info["file_type"] = file_type

def del_book(book):
    dir = book.father
    if "file_type" in book.info:
        os.remove("./bookfiles/" + book.info["title"].replace(": ", "：") + "." + book.info["file_type"])
    dir.remove(book)

def search_online(keyword): # 运行在线搜索爬虫
    os.system(r"search_spider.bat " + keyword)
    


if __name__ == '__main__':
    root, hashtable = __init__()
    # search_online("python")
    # add_book(root)
    # root.sort("title")
    # download_book(root.sons[1])
    # temp = hashtable.search(root.sons[1].info["title"])
    # print(temp.info["authors"])
    # del_book(temp)
    # add_dir(root, "learning")
    # __finish__()
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())
