import json
import libnum

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

class hash:
    def __init__(self): 
        self.p = libnum.generate_prime(size = 10, k=25) # 生成在1000左右的随机质数
        self.list = []

    def calc_hash(self, item): # 计算哈希值
        title = item.info['title']
        title_bytes = title.encode("utf-8")
        value = int.from_bytes(title_bytes, byteorder = 'little', signed = False) % self.p
        return value

    def create_hashtable(self, root): # 初始化时调用，传入root, 递归构造哈希表
        for son in root.sons:
            self.insert(son)
            if son.is_dir:
                self.create_hashtable(son)

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

    def search(self, title):   # 查找，找到返回treenode，找不到返回-1
        title_bytes = title.encode("utf-8")
        hash_value = int.from_bytes(title_bytes, byteorder = 'little', signed=False) % self.p
        length = len(self.list)
        if hash_value > length - 1:
            return -1
        for item in self.list[hash_value]:
            if item.info['title'] == title:
                return item
        return -1

def cmp(a, b, key):
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