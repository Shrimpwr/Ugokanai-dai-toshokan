# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Shrimpwr\Desktop\Study\softwaredev_course_design\source\UI\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(829, 550)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(150, 0, 681, 551))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, -10, 151, 561))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btn_search = QtWidgets.QPushButton(self.groupBox)
        self.btn_search.setGeometry(QtCore.QRect(0, 180, 151, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.btn_search.setFont(font)
        self.btn_search.setObjectName("btn_search")
        self.btn_manage = QtWidgets.QPushButton(self.groupBox)
        self.btn_manage.setGeometry(QtCore.QRect(0, 320, 151, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.btn_manage.setFont(font)
        self.btn_manage.setObjectName("btn_manage")
        self.groupBox.raise_()
        self.frame.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "動かない大図書館"))
        self.btn_search.setText(_translate("Form", "在线搜索"))
        self.btn_manage.setText(_translate("Form", "本地书架"))
