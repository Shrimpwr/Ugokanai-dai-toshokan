import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
import download
import json
import books_manage as manage
import Ui_untitled

def __init__(): # 程序初始化
    root = manage.treenode(True, {"title":"root"}, [])
    with open("./data/booklist.json", "r", encoding='utf-8') as f: 
        filestr = f.read()
        if len(filestr): root.read_file(filestr)
    return root

def __finish__(root): # 程序退出，导出booklist文件
    with open("./data/booklist.json", "w", encoding='utf-8') as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))

def addbook(dir): # 向目录中添加书籍
    with open("./data/search_results.json", "r", encoding='utf-8') as f:
        results = json.load(f)
        for book in results:
            dir.insert(manage.treenode(False, book, []))

if __name__ == '__main__':
    root = __init__()
    # addbook(root)
    # root.sort("authors")
    download.downloadfile(root.sons[0].info["link"], root.sons[0].info["title"])
    
    __finish__(root)

    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
    pass