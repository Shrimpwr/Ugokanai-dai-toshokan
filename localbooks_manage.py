class node:     #节点的定义及操作方法
    def __init__(self):
        pass

    def update(self,item):
        pass

    def sort(self):     #对节点中的数据进行排序
        pass

class tree: #实现文件夹操作，支持创建，删除文件夹，以及文件夹内元素（书籍或文件夹）的插入、删除
    def __init__(self,items): # 要从
        pass

    def sort(self):
        pass

def qsort(items, key): # 使用快速排序算法将items内的元素按关键字key排序
    if len(items) >= 2:
        mid = items[len(items)//2]
        left = []
        right = []
        items.remove(mid)
        for each in items:
            if cmp(each[key], mid[key], key):
                right.append(each)
            else:
                left.append(each)
        return qsort(left)+[mid]+qsort(right)
    else:
        return items

def cmp(a, b, key):
    if key == "title":
        return a[key] <= b[key]
    elif key == "authors":
        return a[key][0] <= b[key][0] # 作者可能有多个的情况，只比较第一个作者
    pass