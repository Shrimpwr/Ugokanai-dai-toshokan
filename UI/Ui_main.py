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
        Form.resize(1407, 846)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(220, 0, 1181, 851))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, -10, 221, 861))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btn_search = QtWidgets.QPushButton(self.groupBox)
        self.btn_search.setGeometry(QtCore.QRect(0, 470, 221, 71))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_search.setFont(font)
        self.btn_search.setObjectName("btn_search")
        self.btn_manage = QtWidgets.QPushButton(self.groupBox)
        self.btn_manage.setGeometry(QtCore.QRect(0, 400, 221, 71))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.btn_manage.setFont(font)
        self.btn_manage.setObjectName("btn_manage")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 201, 331))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("c:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Patchouli_Knowledge2.jpg.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(70, 825, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.groupBox.raise_()
        self.frame.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "動かない大図書館"))
        self.btn_search.setText(_translate("Form", "在线搜索"))
        self.btn_manage.setText(_translate("Form", "本地书架"))
        self.label_2.setText(_translate("Form", "v 1.00"))
