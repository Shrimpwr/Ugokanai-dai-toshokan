import os
import sys
import json
import requests
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView

# 导入UI
from UI.Ui_main import Ui_Form
from UI.Ui_book_page import Ui_book_page
from UI.Ui_search_page import Ui_search_page
from UI.Ui_result_page import Ui_result_page
# 导入功能模块
from books_manage import __init__, __finish__, add_book, add_dir, download_book, del_book, search_online, del_dir

class Signal(QObject): # 自定义信号
    search_done = pyqtSignal()

class FrameBookPage(QWidget, Ui_book_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = root
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 500) 
        self.tableWidget.setColumnWidth(2, 260)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setText("root")
        self.show_dircontent(root)
        self.controller()

    def controller(self):
        self.tableWidget.cellDoubleClicked.connect(self.doubleclk)
        pass
    
    @pyqtSlot(int, int)
    def doubleclk(self, row, column):
        pass

    def show_dircontent(self, dir):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        for i, node in enumerate(dir.sons):
            title = node.info["title"]
            cover = QtWidgets.QLabel("")
            if node.is_dir == False:
                authors = ",".join(node.info["authors"])
                if node.info["coverlink_s"] != 'https://zh.1lib.org/img/book-no-cover.png':
                    cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/normal_cover/" + node.info["coverlink_s"][-36:]).scaled(100,150))
                else:
                    cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/book-no-cover.png").scaled(100,140))
            else:
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/folder.png").scaled(100,100))
                authors = ''
            
            self.tableWidget.insertRow(i)
            self.tableWidget.setCellWidget(i, 0, cover)
            cover.setAlignment(Qt.AlignCenter)
            
            title_item = QTableWidgetItem(title)   
            title_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)       
            self.tableWidget.setItem(i, 1, title_item)

            authors_item = QTableWidgetItem(authors)
            authors_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 2, authors_item)
        pass


class FrameSearchPage(QWidget, Ui_search_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class FrameResultPage(QWidget, Ui_result_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_agree.hide()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        # self.tableWidget.setStyleSheet("QTableWidget{outline:0px;}")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 500) 
        self.tableWidget.setColumnWidth(2, 255)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.controller()

    def controller(self):
        self.btn_add2lib.clicked.connect(self.selectDir)
        self.btn_add2lib.clicked.connect(self.add2lib)

    def add2lib(self):
        selections = self.tableWidget.selectionModel()
        selectedsList = selections.selectedRows()
        print(selectedsList)
        
        pass

    def selectDir(self):
        self.btn_add2lib.hide()
        self.btn_agree.show()
        pass

    def prepare(self): # 读取搜索结果并获取封面
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        with open("./data/search_results.json", "r", encoding='utf-8') as f:
            self.resultlist = json.load(f)
        self.showTable(self.resultlist)

    def showTable(self, resultlist):
        for i, book in enumerate(resultlist):
            title = book["title"]
            authors = ",".join(book["authors"])
            cover = QtWidgets.QLabel("")
            inlib = False
            local_have = hashtable.search(book["title"])
            if local_have != -1:
                for i in local_have:
                    if i.info["id"] == book["id"]:
                        inlib = True
            self.tableWidget.insertRow(i)

            self.tableWidget.setCellWidget(i, 0, cover)
            cover.setAlignment(Qt.AlignCenter)
            if book["coverlink_s"] != 'https://zh.1lib.org/img/book-no-cover.png':
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/normal_cover/" + book["coverlink_s"][-36:]).scaled(100,150))
            else:
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/book-no-cover.png").scaled(100,140))

            title_item = QTableWidgetItem(title)   
            title_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)       
            self.tableWidget.setItem(i, 1, title_item)

            authors_item = QTableWidgetItem(authors)
            authors_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 2, authors_item)

            inlib_item = QTableWidgetItem(str(inlib))
            inlib_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 3, inlib_item)
    
class MainWidget(QWidget, Ui_Form):
    # 主窗口
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 实例化一个堆叠布局
        self.qsl = QStackedLayout(self.frame)
        self.groupBox.setStyleSheet("border:0px")
        # 实例化分页面
        self.book = FrameBookPage()
        self.search = FrameSearchPage()
        self.result = FrameResultPage()
        # 加入到布局中
        self.qsl.addWidget(self.book)
        self.qsl.addWidget(self.search)
        self.qsl.addWidget(self.result)
        # 控制函数
        self.sig = Signal() 
        self.controller()

    def controller(self): #将事件连接到槽函数
        self.btn_manage.clicked.connect(self.switch)
        self.btn_search.clicked.connect(self.switch)
        self.search.pushButton.clicked.connect(self.run_search)
        self.sig.search_done.connect(self.result.prepare)

    def switch(self): #切换页面
        sender = self.sender().objectName()

        index = {
            "btn_manage": 0,
            "btn_search": 1,
        }

        self.qsl.setCurrentIndex(index[sender])
    
    def run_search(self): # 进行搜索
        keyword = self.search.lineEdit.text()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('提示')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('将要运行爬虫，基于当前网络情况，可能需要一段时间，请勿关闭程序，按OK继续')
        msgBox.exec()
        # search_online(keyword)
        self.sig.search_done.emit() # 发出信号让resultpage准备内容
        self.qsl.setCurrentIndex(2) # 搜索完成，跳转到search_result，展示搜索结果
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None: # 关闭时保存文件
        super().closeEvent(a0)
        __finish__(root)


if __name__ == '__main__':
    root, hashtable = __init__()
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    
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

    sys.exit(app.exec_())
