import os
import sys
import json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

from books_manage import __init__, __finish__, add_book, add_dir, download_book, del_book, search_online, del_dir
from UI.stacklayout import MainWidget



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
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        __finish__(root)


if __name__ == '__main__':
    root, hashtable = __init__()
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())
    # with open("./data/search_results.json", "r", encoding='utf-8') as f:
    #     results = json.load(f)
    #     for book in results:
    #         add_book(root, book, hashtable)

    # add_dir(root, "learning", hashtable)

    # root.sort("title")
    
    # download_book(root.sons[1])

    # temp = hashtable.search(root.sons[1].info["title"])

    # del_book(temp[0], hashtable)

    # del_dir(root, root.sons[0], hashtable)

    # 以上功能需要与前端连接
