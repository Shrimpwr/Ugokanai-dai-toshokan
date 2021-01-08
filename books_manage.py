import os
import json
import libnum
import download
import requests
import wget
import subprocess

class treenode: # 利用树形结构实现文件夹操作，支持创建，删除文件夹，以及文件夹内元素（书籍或文件夹）的插入、删除
    def __init__(self, is_dir, info, sons):
        self.is_dir = is_dir
        self.info = info # 存放当前结点信息的字典
        self.sons = sons # 文件夹中的元素
        self.father = self

    def insert(self, son):
        if son.is_dir:
            self.sons = [son] + self.sons # 文件夹默认排在最前面
        else:
            self.sons.append(son)
        son.father = self

    def remove(self, son):
        self.sons.remove(son)
        del son

    def read_file(self, file): # 从文件读入本地书籍目录, 用到了json与实体类的互转
        data = json.loads(file)
        self.is_dir = data["is_dir"]
        self.info = data["info"]
        for each_son in data["sons"]: # 递归调用，建树
            son = treenode(False, {}, [])
            each_son_str = json.dumps(each_son) # 将儿子的dict再转成字符串，递归解析，用json.dumps()而不直接str()是为了避免单引号在后续解析中报错。
            son.read_file(each_son_str)
            self.insert(son)
        del data

    def export_to_file(self): # 书籍目录更新时，需要将书籍目录导出至json文件
        data = {}
        data["is_dir"] = self.is_dir
        data["info"] = self.info
        data["sons"] = []
        for each_son in self.sons: # 递归调用，建树
            data["sons"].append(each_son.export_to_file())
        return data

    def sort(self, key):
        self.sons = qsort(self.sons, key)

class hash: # hash表，支持从根目录直接创建整个表，或是在表中插入，移除单个元素（书籍或文件夹）
    def __init__(self): 
        self.p = libnum.generate_prime(size = 10, k=25) # 生成在1000左右的随机质数
        self.list = []

    def calc_hash(self, item): # 计算哈希值
        title = item.info['title']
        title_bytes = title.encode("utf-8")
        value = int.from_bytes(title_bytes, byteorder = 'little', signed = False) % self.p
        return value

    def create_table(self, root): # 初始化时调用，传入root, 递归构造哈希表
        for son in root.sons:
            self.insert(son)
            if son.is_dir:
                self.create_table(son)

    def insert(self, item): # 当书目中添加新书籍时调用，向哈希表中插入新项
        hash_value = self.calc_hash(item)
        length = len(self.list)
        if hash_value > length - 1:
            for j in range (length, hash_value + 1):
                if j == hash_value:
                    self.list.append([item])
                else:
                    self.list.append([])
        else:
            self.list[hash_value].append(item)

    def remove(self, item): # 从表中移除指定项
        hash_value = self.calc_hash(item)
        length = len(self.list)
        if hash_value > length - 1:
            return -1
        for i in self.list[hash_value]:
            if i == item:
                self.list[hash_value].remove(item)

    def search(self, title):   # 按标题精确查找，找到返回treenode，找不到返回-1
        title_bytes = title.encode("utf-8")
        hash_value = int.from_bytes(title_bytes, byteorder = 'little', signed=False) % self.p
        length = len(self.list)
        if hash_value > length - 1:
            return -1
        items = []
        for item in self.list[hash_value]:
            if item.info['title'] == title:
                items.append(item)
        if len(items) > 0:
            return items
        return -1

def cmp(a, b, key): # 快速排序使用的比较函数
    if a.is_dir == True and b.is_dir == True:
        return a.info["title"] <= b.info["title"]

    elif a.is_dir == False and b.is_dir == False:
        if key == "title":
            return a.info[key] <= b.info[key]
        elif key == "authors":
            return a.info[key][0] <= b.info[key][0] # 作者可能有多个的情况，只比较第一个作者

    else: # 一个是文件夹而一个是书籍的情况，默认将文件夹排在前面
        return a.is_dir

def qsort(list, key): # 使用快速排序算法将list内的元素按关键字key排序
    if len(list) >= 2:
        mid = list[len(list) // 2]
        left = []
        right = []
        list.remove(mid)
        for item in list:
            if cmp(item, mid, key):
                left.append(item)
            else:
                right.append(item)
        return qsort(left, key) + [mid] + qsort(right, key)
    else:
        return list

def __init__(): # 程序初始化，建立根目录与哈希表
    if not os.path.exists("./data/booklist.json"):
        f = open("./data/booklist.json", "wb")
        f.close()

    root = treenode(True, {"title":"root"}, [])
    with open("./data/booklist.json", "r", encoding='utf-8') as f: 
        filestr = f.read()
        if len(filestr): root.read_file(filestr)

    hashtable = hash()
    hashtable.insert(root)
    hashtable.create_table(root)
    return root, hashtable

def __finish__(root): # 程序退出，导出booklist文件
    with open("./data/booklist.json", "w", encoding='utf-8') as f:
        data = root.export_to_file()
        f.write(json.dumps(obj=data,ensure_ascii=False))

def add_book(dir, book, hashtable): # 向目录中添加书籍
    temp = hashtable.search(book["title"])
    if temp != -1:
        for i in temp:
            if i.info["id"] == book["id"]:
                return -1
    newbook = treenode(False, book, [])
    dir.insert(newbook)
    hashtable.insert(newbook)
    if book["coverlink_l"] != "https://zh.1lib.org/img/book-no-cover.png":
        url = book["coverlink_l"]
        COOKIES = {
        "remix_userkey": "9df24a5274a9f199658810aaa7b3e591",
        "remix_userid": "6118916"
        }   
        res = requests.get(url, cookies = COOKIES)
        path = "./bookfiles/covers/local_cover/" + book["coverlink_l"][-36:]
        # wget.download(book["coverlink_l"], out = path)
        with open(path, 'wb') as f:
            f.write(res.content)
    
def del_book(book, hashtable): # 删除指定书籍
    dir = book.father
    if "file_type" in book.info:
        os.remove("./bookfiles/" + book.info["title"].replace(": ", "：") + "." + book.info["file_type"])
    hashtable.remove(book)
    dir.remove(book)

def add_dir(father_dir, title, hashtable): # 向指定上级目录中添加标题为title的新文件夹
    temp = hashtable.search(title)
    if temp != -1:
        for i in temp: 
            if i in father_dir.sons: # 同一个上级目录下不允许存在两个同名文件夹
                return -1  
    newdir = treenode(True, {"title":title}, [])
    father_dir.insert(newdir)
    hashtable.insert(newdir)

def del_dir(father_dir, dir, hashtable): # 从指定上级目录中删除指定文件夹
    if dir.father == father_dir:
        hashtable.remove(dir)
        father_dir.remove(dir)
        
def download_book(book): # 下载指定书籍
    file_type = download.downloadfile(book.info["link"], book.info["title"])
    book.info["file_type"] = file_type

def search_online(keyword): # 运行在线搜索爬虫
    os.system(r"cd creeper && scrapy crawl zlib_search -a keyword=" + keyword + " -a page=1")

if __name__ == "__main__":
    search_online("python")