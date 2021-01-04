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