import json

class treenode: # 利用树形结构实现文件夹操作，支持创建，删除文件夹，以及文件夹内元素（书籍或文件夹）的插入、删除
    def __init__(self, is_dir, info, sons):
        self.is_dir = is_dir
        self.info = info # 存放当前结点信息的字典
        self.sons = sons # 文件夹中的元素
        self.father = self

    def insert(self, son):
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

class Hash:
    def __init__(self):
        self.list = []
        self.p = 65537

    def get_hash(self,item):
        src = item.info['title']
        temp = src.encode("utf-8")
        i = int.from_bytes(temp, byteorder = 'little', signed = False)
        m = i % self.p
        return m

    def create_hashtable(self, root): #传入root, 递归构造哈希表
        for item in root.sons:
            i = self.get_hash(item)
            l = len(self.list)
            if i > l - 1:
                for j in range (l, i + 1):
                    if j == i:
                        self.list.append([item])
                    else:
                        self.list.append([])
            else:
                self.list[i].append(item)

    def search(self,src):   # 精确查找,找到返回treenode，找不到返回-1
        temp = src.encode("utf-8")
        n = int.from_bytes(temp, byteorder = 'little', signed=False)
        i = n % self.p
        for each in self.list[i]:
            if each['title'] == src:
                return each
        return -1

def qsort(items, key): # 使用快速排序算法将items内的元素按关键字key排序
    if len(items) >= 2:
        mid = items[len(items) // 2]
        left = []
        right = []
        items.remove(mid)
        for each in items:
            if cmp(each, mid, key):
                left.append(each)
            else:
                right.append(each)
        return qsort(left, key) + [mid] + qsort(right, key)
    else:
        return items

def cmp(a, b, key):
    if a.is_dir == True and b.is_dir == True:
        return a.info["title"] <= b.info["title"]
    elif a.is_dir == False and b.is_dir == False:
        if key == "title":
            return a.info[key] <= b.info[key]
        elif key == "authors":
            return a.info[key][0] <= b.info[key][0] # 作者可能有多个的情况，只比较第一个作者
    else:
        return a.is_dir