import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
import download
import json
import books_manage as manage
import Ui_untitled


if __name__ == '__main__':
    root = manage.treenode(True, {"title":"root"}, [])
    book = manage.treenode(False, {"title": "Learn Python in One Day and Learn It Well: Python for Beginners with Hands-on Project. The only book you need to start coding in Python immediately", "link": "https://zh.1lib.org/book/2519956/2c2800", "coverlink_s": "https://covers.zlibcdn2.com/covers100/books/3d/f2/a0/3df2a0de6424a738e4cdbd41b537de28.jpg", "coverlink_l": "https://covers.zlibcdn2.com/covers200/books/3d/f2/a0/3df2a0de6424a738e4cdbd41b537de28.jpg", "authors": ["Jamie Chan"]}, [])
    book2 = manage.treenode(False, {"title": "Python Basics: A Self-Teaching Introduction", "link": "https://zh.1lib.org/book/3641986/812370", "coverlink_s": "https://covers.zlibcdn2.com/covers100/books/f0/d3/6d/f0d36d571089b7f21c8e4a117b0440f5.jpg", "coverlink_l": "https://covers.zlibcdn2.com/covers200/books/f0/d3/6d/f0d36d571089b7f21c8e4a117b0440f5.jpg", "authors": ["H. Bhasin"]}, [])
    root.insert(book)
    root.insert(book2)
    root.sort("authors")
    print(root.sons[0].info["authors"], root.sons[1].info["authors"])
    with open("./data/booklist.json", "w") as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))
    with open("./data/booklist.json", "r") as f: 
        filestr = f.read()
        root.read_file(filestr)
    print(root)
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
    pass