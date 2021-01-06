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
        self.tableWidget.verticalHeader().hide()
        self.current_dir = root
        self.btn_agree.hide()
        self.btn_disagree.hide()
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 528) 
        self.tableWidget.setColumnWidth(2, 260)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setText("root")
        self.show_dircontent(root, self.tableWidget)
        self.controller()

    def controller(self):
        self.tableWidget.cellDoubleClicked.connect(self.doubleclk)
        self.tableWidget.cellClicked.connect(self.clk)
        pass
    
    @pyqtSlot(int, int)
    def doubleclk(self, row, column):
        if row == 0 and self.current_dir != root:
            s = self.label.text()
            leng = len(self.current_dir.info["title"]) + 3
            s = s[0:-leng]
            self.label.setText(s)
            self.current_dir = self.current_dir.father
            self.show_dircontent(self.current_dir, self.tableWidget)
        else:
            node = self.current_dir.sons[row]
            if node.is_dir:
                s = self.label.text()
                s += " > " + node.info["title"]
                self.label.setText(s)
                self.current_dir = node
                self.show_dircontent(self.current_dir, self.tableWidget)

    @pyqtSlot(int, int)
    def clk(self, row, column):
        if len(self.current_dir.sons) > row:
            node = self.current_dir.sons[row]
            cover_l = self.coverlabel
            pass

    def show_dircontent(self, dir, table):
        while table.rowCount() > 0:
            table.removeRow(0)
        
        for i, node in enumerate(dir.sons):
            title = node.info["title"]
            cover = QtWidgets.QLabel("")
            if node.is_dir == False:
                authors = ",".join(node.info["authors"])
                if node.info["coverlink_s"] != 'https://zh.1lib.org/img/book-no-cover.png':
                    cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/normal_cover/" + node.info["coverlink_s"][-36:]).scaled(80,115))
                else:
                    cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/book-no-cover.png").scaled(80,115))
            else:
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/folder.png").scaled(80,80))
                authors = ''
            
            table.insertRow(i)
            table.setCellWidget(i, 0, cover)
            cover.setAlignment(Qt.AlignCenter)
            
            title_item = QTableWidgetItem(title)   
            title_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)       
            table.setItem(i, 1, title_item)

            authors_item = QTableWidgetItem(authors)
            authors_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(i, 2, authors_item)

        if dir != root:
            table.insertRow(0)

            cover = QtWidgets.QLabel("")
            cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/folder.png").scaled(80,80))
            table.setCellWidget(0, 0, cover)
            cover.setAlignment(Qt.AlignCenter)

            title = "上级目录"
            title_item = QTableWidgetItem(title)   
            title_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)       
            table.setItem(0, 1, title_item)

            authors = ''
            authors_item = QTableWidgetItem(authors)
            authors_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(0, 2, authors_item)
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
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 528) 
        self.tableWidget.setColumnWidth(2, 255)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

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
                for j in local_have:
                    if j.info["id"] == book["id"]:
                        inlib = True
            self.tableWidget.insertRow(i)

            self.tableWidget.setCellWidget(i, 0, cover)
            cover.setAlignment(Qt.AlignCenter)
            if book["coverlink_s"] != 'https://zh.1lib.org/img/book-no-cover.png':
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/normal_cover/" + book["coverlink_s"][-36:]).scaled(80,115))
            else:
                cover.setPixmap(QtGui.QPixmap("./bookfiles/covers/book-no-cover.png").scaled(100,115))

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
        self.result.btn_add2lib.clicked.connect(self.selectdir)
        self.book.btn_agree.clicked.connect(self.confirm_add)
        self.book.btn_disagree.clicked.connect(self.confirm_add)

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
        search_online(keyword)
        self.sig.search_done.emit() # 发出信号让resultpage准备内容
        self.qsl.setCurrentIndex(2) # 搜索完成，跳转到search_result，展示搜索结果
    
    def selectdir(self):
        selections = self.result.tableWidget.selectionModel()
        selectedsList = selections.selectedRows()
        if len(selectedsList) == 0:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('错误')
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('还没有选中图书！')
            msgBox.exec()
            return
        self.qsl.setCurrentIndex(0)
        self.book.coverlabel.hide()
        s = self.book.label.text()
        s = "添加到：" + s
        self.book.label.setText(s)
        self.book.btn_download.hide()
        self.book.btn_agree.show()
        self.book.btn_disagree.show()
        self.book.current_dir = root
        self.book.show_dircontent(root, self.book.tableWidget)
    
    def confirm_add(self):
        self.book.coverlabel.show()
        s = self.book.label.text()
        s = s[4:]
        self.book.label.setText(s)
        self.book.label.setText(s)
        self.book.btn_agree.hide()
        self.book.btn_disagree.hide()
        self.book.btn_download.show()
        if self.sender() == self.book.btn_agree:
            selections = self.result.tableWidget.selectionModel()
            selectedsList = selections.selectedRows()
            for r in selectedsList:
                add_book(self.book.current_dir, self.result.resultlist[r.row()], hashtable)
            self.book.show_dircontent(self.book.current_dir, self.book.tableWidget)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None: # 关闭时保存文件
        super().closeEvent(a0)
        __finish__(root)


if __name__ == '__main__':
    root, hashtable = __init__()
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()

    # add_dir(root, "learning", hashtable)

    # root.sort("title")
    
    # download_book(root.sons[1])

    # temp = hashtable.search(root.sons[1].info["title"])

    # del_book(temp[0], hashtable)

    # del_dir(root, root.sons[0], hashtable)

    # 以上功能需要与前端连接

    sys.exit(app.exec_())
