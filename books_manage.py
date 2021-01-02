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

    def readfile(self, file): # 从文件读入本地书籍目录, 用到了json与实体类的互转
        data = json.load(file, object_hook=self.dict2node)
        self.is_dir = data["is_dir"]
        self.info = data["info"]
        for i in data["sons"]: # 递归调用，建树
            son = treenode(False, {}, [])
            son.readfile(str(i))
            self.insert(son)
        del data

    def dict2node(self, d):
        return treenode(d['is_dir'], d['info'], d['sons'])

    def export_to_file(self, filename): # 书籍目录更新时，需要将书籍目录导出至文件
        # with open("./data/" + filename, "w") as f: f.write(json.dumps(obj=self.__dict__,ensure_ascii=False))
        pass

    def sort(self, key):
        self.sons = qsort(self.sons, key)
        
class hash:
    pass

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
    
# sys.path.append('C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source') 
# from books_manage import treenode