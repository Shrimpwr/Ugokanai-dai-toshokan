# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Shrimpwr\Desktop\Study\softwaredev_course_design\source\UI\book_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_book_page(object):
    def setupUi(self, book_page):
        book_page.setObjectName("book_page")
        book_page.resize(1179, 841)
        self.tableWidget = QtWidgets.QTableWidget(book_page)
        self.tableWidget.setGeometry(QtCore.QRect(0, 30, 931, 811))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.label = QtWidgets.QLabel(book_page)
        self.label.setGeometry(QtCore.QRect(0, 0, 911, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.coverlabel = QtWidgets.QLabel(book_page)
        self.coverlabel.setGeometry(QtCore.QRect(960, 260, 191, 281))
        self.coverlabel.setText("")
        self.coverlabel.setObjectName("coverlabel")
        self.btn_download = QtWidgets.QPushButton(book_page)
        self.btn_download.setGeometry(QtCore.QRect(1000, 640, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_download.setFont(font)
        self.btn_download.setObjectName("btn_download")
        self.btn_agree = QtWidgets.QPushButton(book_page)
        self.btn_agree.setGeometry(QtCore.QRect(1000, 320, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_agree.setFont(font)
        self.btn_agree.setObjectName("btn_agree")
        self.btn_disagree = QtWidgets.QPushButton(book_page)
        self.btn_disagree.setGeometry(QtCore.QRect(1000, 400, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_disagree.setFont(font)
        self.btn_disagree.setObjectName("btn_disagree")
        self.lab_proval = QtWidgets.QLabel(book_page)
        self.lab_proval.setGeometry(QtCore.QRect(970, 610, 171, 20))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.lab_proval.setFont(font)
        self.lab_proval.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_proval.setObjectName("lab_proval")
        self.btn_hash = QtWidgets.QPushButton(book_page)
        self.btn_hash.setGeometry(QtCore.QRect(1000, 130, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_hash.setFont(font)
        self.btn_hash.setObjectName("btn_hash")
        self.btn_back = QtWidgets.QPushButton(book_page)
        self.btn_back.setGeometry(QtCore.QRect(1000, 190, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.lineEdit = QtWidgets.QLineEdit(book_page)
        self.lineEdit.setGeometry(QtCore.QRect(80, 210, 801, 51))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.btn_hashagree = QtWidgets.QPushButton(book_page)
        self.btn_hashagree.setGeometry(QtCore.QRect(1000, 130, 111, 51))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_hashagree.setFont(font)
        self.btn_hashagree.setObjectName("btn_hashagree")

        self.retranslateUi(book_page)
        QtCore.QMetaObject.connectSlotsByName(book_page)

    def retranslateUi(self, book_page):
        _translate = QtCore.QCoreApplication.translate
        book_page.setWindowTitle(_translate("book_page", "Form"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("book_page", "新建行"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("book_page", "Cover"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("book_page", "Title"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("book_page", "Authors"))
        self.label.setText(_translate("book_page", "TextLabel"))
        self.btn_download.setText(_translate("book_page", "下载"))
        self.btn_agree.setText(_translate("book_page", "确定"))
        self.btn_disagree.setText(_translate("book_page", "取消"))
        self.lab_proval.setText(_translate("book_page", "TextLabel"))
        self.btn_hash.setText(_translate("book_page", "查找"))
        self.btn_back.setText(_translate("book_page", "取消"))
        self.btn_hashagree.setText(_translate("book_page", "确定"))
