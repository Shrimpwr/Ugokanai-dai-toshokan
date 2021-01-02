import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
import download
import json
import books_manage as manage
import Ui_untitled


if __name__ == '__main__':
    root = manage.treenode(True, {"title":"root"}, [])
    book = manage.treenode(False, {"title": "村上春树长篇代表作品集：且听风吟、1973年的弹子球、寻羊冒险记、世界尽头与冷酷仙境、挪威的森林、舞舞舞、国境以南太阳以西、奇鸟行状录、斯普特尼克恋人、海边的卡夫卡", "link": "https://zh.1lib.org/book/5580286/8dc71c", "coverlink_s": "https://covers.zlibcdn2.com/covers100/books/57/64/c6/5764c646519da244fd06bd3ebbe95ae2.jpg", "coverlink_l": "https://covers.zlibcdn2.com/covers200/books/57/64/c6/5764c646519da244fd06bd3ebbe95ae2.jpg", "authors": ["村上春树", "林少华"]}, [])
    book2 = manage.treenode(False, {"title": "Python Basics: A Self-Teaching Introduction", "link": "https://zh.1lib.org/book/3641986/812370", "coverlink_s": "https://covers.zlibcdn2.com/covers100/books/f0/d3/6d/f0d36d571089b7f21c8e4a117b0440f5.jpg", "coverlink_l": "https://covers.zlibcdn2.com/covers200/books/f0/d3/6d/f0d36d571089b7f21c8e4a117b0440f5.jpg", "authors": ["H. Bhasin"]}, [])
    root.insert(book)
    root.insert(book2)
    root.sort("authors")
    print(root.sons[0].info["authors"], root.sons[1].info["authors"])
    with open("./data/booklist.json", "w", encoding='utf-8') as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))
    with open("./data/booklist.json", "r", encoding='utf-8') as f: 
        filestr = f.read()
        root.read_file(filestr)
    print(root.__dict__)
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
    pass