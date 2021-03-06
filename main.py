import os
import sys
import json
from tempfile import tempdir
import requests
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView, QMenu, QInputDialog
from scrapy.selector.unified import SelectorList

# 导入UI
from UI.Ui_main import Ui_Form
from UI.Ui_book_page import Ui_book_page
from UI.Ui_search_page import Ui_search_page
from UI.Ui_result_page import Ui_result_page
# 导入功能模块
from books_manage import __init__, __finish__, add_book, add_dir, download_book, del_book, search_online, del_dir, treenode


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
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 548) 
        self.tableWidget.setColumnWidth(2, 260)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # font = QtGui.QFont()
        # font.setFamily("Co")
        # font.setPointSize(10)
        # self.label.setFont(font)
        self.label.setText("root")
        self.lab_proval.setText('')
        self.btn_download.hide()
        self.lineEdit.hide()
        self.btn_back.hide()
        self.btn_hashagree.hide()
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu) 
        self.show_dircontent(root, self.tableWidget)
        self.controller()

    def controller(self):
        self.tableWidget.cellDoubleClicked.connect(self.doubleclk)
        self.tableWidget.cellClicked.connect(self.clk)
        self.btn_download.clicked.connect(self.downloadthis)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sort)
        self.btn_hash.clicked.connect(self.pre_hashsearch)
        self.btn_hashagree.clicked.connect(self.hashsearch)
        self.btn_back.clicked.connect(self.after_hashsearch)
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
    
    def showContextMenu(self, pos):  # 创建右键菜单
        self.tableWidget.contextMenu = QMenu(self)
        self.actionA = self.tableWidget.contextMenu.addAction(u'创建文件夹')
        self.actionB = self.tableWidget.contextMenu.addAction(u'删除')
        self.tableWidget.contextMenu.popup(QtGui.QCursor.pos()) 
        self.actionA.triggered.connect(self.create_dir)
        self.actionB.triggered.connect(self.delete_item)
        self.tableWidget.contextMenu.show()

    def create_dir(self):
        text, ok = QInputDialog.getText(self, '创建文件夹', '请输入文件夹名:')
        if ok:
            msg = add_dir(self.current_dir, text, hashtable)
            if msg == -1:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('错误')
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('添加错误，请检查文件夹是否重名！')
                msgBox.exec()
            else:
                self.show_dircontent(self.current_dir, self.tableWidget)

    def delete_item(self):
        selections = self.tableWidget.selectionModel()
        selectedsList = selections.selectedRows()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('错误')
        msgBox.setIcon(QMessageBox.Warning)
        if len(selectedsList) == 0:
            msgBox.setText('还没有选中要删除的项目！')
            msgBox.exec()
            return
        selected = selectedsList[0]
        num = selected.row()
        if (self.current_dir != root and num == 0):
            msgBox.setText('不能删除上级文件夹！')
            msgBox.exec()
            return
        if self.current_dir != root and num > 0:
            num -= 1
        item = self.current_dir.sons[num]
        if item.is_dir == False:
            del_book(item, hashtable)
            self.show_dircontent(self.current_dir, self.tableWidget)
            return
        else:
            if len(item.sons) > 0:
                msgBox.setText('不能删除非空文件夹！')
                msgBox.exec()
            else:
                del_dir(self.current_dir, item, hashtable)
                self.show_dircontent(self.current_dir, self.tableWidget)
                return

    def pre_hashsearch(self):
        self.btn_hash.hide()
        self.lineEdit.show()
        self.btn_hashagree.show()
        self.btn_back.show()

    def after_hashsearch(self, temp_dir = None):
        self.btn_hash.show()
        self.lineEdit.hide()
        self.lineEdit.setText("")
        self.btn_hashagree.hide()
        self.btn_back.hide()
        if temp_dir != None:
            del temp_dir

    def hashsearch(self):
        keyword = self.lineEdit.text()
        temp = hashtable.search(keyword)
        temp_dir = treenode(True, {"title": "search results"}, [])
        if self.label.text() == "search results":
            temp_dir.father = self.current_dir.father
        else:
            temp_dir.father = self.current_dir
        self.current_dir = temp_dir
        self.label.setText("search results")
        if temp != -1:
            for i in temp:
                temp_dir.sons.append(i)
        self.show_dircontent(temp_dir, self.tableWidget)
        self.after_hashsearch(temp_dir)

    @pyqtSlot(int, int)
    def doubleclk(self, row, column):
        if row == 0 and self.current_dir != root:
            s = self.label.text()
            if "search results" in s:
                    s = ''
                    fa = self.current_dir.father
                    while fa != root:
                        s = ' > ' + fa.info["title"] + s
                        fa = fa.father
                    s = 'root' + s
            else:
                leng = len(self.current_dir.info["title"]) + 3
                s = s[0:-leng]
            self.label.setText(s)
            self.current_dir = self.current_dir.father
            self.show_dircontent(self.current_dir, self.tableWidget)

        else:
            if self.current_dir != root and row > 0:
                row = row - 1
            node = self.current_dir.sons[row]
            if node.is_dir:
                s = self.label.text()
                if "search results" in s:
                    s = ''
                    fa = node.father
                    while fa != root:
                        s = ' > ' + fa.info["title"] + s
                        fa = fa.father
                    s = 'root' + s
                s += " > " + node.info["title"]
                self.label.setText(s)
                self.current_dir = node
                self.show_dircontent(self.current_dir, self.tableWidget)

    @pyqtSlot(int, int)
    def clk(self, row, column):
        if row == 0 and self.current_dir != root:
            self.btn_download.hide()
            cover_l = self.coverlabel
            cover_l.setPixmap(QtGui.QPixmap("./bookfiles/covers/folder.png").scaled(190,190))
            self.lab_proval.setText('')
        else:
            if self.current_dir != root and row > 0:
                row = row - 1
            node = self.current_dir.sons[row]
            if node.is_dir == False:
                if self.btn_agree.isHidden():
                    self.btn_download.show()
                    if "file_type" in node.info:
                        self.btn_download.setText("已下载")
                        self.btn_download.setEnabled(False)
                    else:
                        self.btn_download.setText("下载")
                        self.btn_download.setEnabled(True)
                    cover_l = self.coverlabel
                    if node.info["coverlink_l"] != "https://zh.1lib.org/img/book-no-cover.png":
                        cover_l.setPixmap(QtGui.QPixmap("./bookfiles/covers/local_cover/" + node.info["coverlink_l"][-36:]).scaled(190,280))
                    else:
                        cover_l.setPixmap(QtGui.QPixmap("./bookfiles/covers/book-no-cover.png").scaled(190,280))
                    self.lab_proval.setText(node.info["property_value"])
            else:
                self.btn_download.hide()
                cover_l = self.coverlabel
                cover_l.setPixmap(QtGui.QPixmap("./bookfiles/covers/folder.png").scaled(190,190))
                self.lab_proval.setText('')

    @pyqtSlot(int)
    def sort(self, column):
        if column == 1:
            self.current_dir.sort("title")
            self.show_dircontent(self.current_dir, self.tableWidget)
        if column == 2:
            self.current_dir.sort("authors")
            self.show_dircontent(self.current_dir, self.tableWidget)

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

    def downloadthis(self):
        selections = self.tableWidget.selectionModel()
        selected = selections.selectedRows()[0]
        num = selected.row()
        if self.current_dir != root and num > 0:
                num -= 1
        download_book(self.current_dir.sons[num])
        __finish__(root)
        self.btn_download.setText("已下载")
        self.btn_download.setEnabled(False)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('提示')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('下载完成！')
        msgBox.exec()

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

        msgBox = QMessageBox()
        msgBox.setWindowTitle('提示')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('搜索完成！')
        msgBox.exec()

class MainWidget(QWidget, Ui_Form):
    # 主窗口
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 实例化一个堆叠布局
        self.qsl = QStackedLayout(self.frame)
        # 实例化分页面
        self.book = FrameBookPage()
        self.search = FrameSearchPage()
        self.result = FrameResultPage()
        # 加入到布局中
        self.qsl.addWidget(self.book)
        self.qsl.addWidget(self.search)
        self.qsl.addWidget(self.result)
        # 外观设置
        self.groupBox.setStyleSheet("border:0px")
        #self.setStyleSheet("background-color:#BBFFFF")
        #self.book.tableWidget.setStyleSheet("border:0px")
        self.setWindowIcon(QtGui.QIcon('./UI/patchouli.png'))
        self.btn_manage.setStyleSheet(
            # "QPushButton{color:rgb(101,153,26)}" #按键前景色
            #"QPushButton{background-color:#00F5FF}"  #按键背景色
            "QPushButton:hover{background-color:#FFFAFA}" #光标移动到上面后的背景色
            # "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
        )
        self.btn_search.setStyleSheet(
            # "QPushButton{color:rgb(101,153,26)}" #按键前景色
            #"QPushButton{background-color:#00F5FF}"  #按键背景色
            "QPushButton:hover{background-color:#FFFAFA}" #光标移动到上面后的背景色
            # "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
        )
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
        self.book.btn_hash.hide()
        self.book.lab_proval.hide()
        self.book.btn_download.hide()
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
        self.book.show_dircontent(self.book.current_dir, self.book.tableWidget)
    
    def confirm_add(self):
        self.book.coverlabel.show()
        s = self.book.label.text()
        s = s[4:]
        self.book.label.setText(s)
        self.book.label.setText(s)
        self.book.btn_agree.hide()
        self.book.btn_disagree.hide()
        self.book.btn_download.show()
        self.book.btn_hash.show()
        self.book.lab_proval.show()
        if self.sender() == self.book.btn_agree:
            selections = self.result.tableWidget.selectionModel()
            selectedsList = selections.selectedRows()
            for r in selectedsList:
                add_book(self.book.current_dir, self.result.resultlist[r.row()], hashtable)
            __finish__(root)
            self.book.show_dircontent(self.book.current_dir, self.book.tableWidget)
            msgBox = QMessageBox()
            msgBox.setWindowTitle('提示')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('添加完成！')
            msgBox.exec()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None: # 关闭时保存文件
        super().closeEvent(a0)
        __finish__(root)


if __name__ == '__main__':
    root, hashtable = __init__()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling) #保持弹出UI的大小
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())
