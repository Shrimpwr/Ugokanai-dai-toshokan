import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import Ui_untitled
import os

if __name__ == '__main__':
    keyword = input()
    os.system(r"search_spider.bat " + keyword)
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())