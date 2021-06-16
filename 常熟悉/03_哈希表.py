# -*- coding:utf-8 -*-
'''
.哈希表的定义
　　这里先说一下哈希（hash）表的定义：哈希表是一种根据关键码去寻找值的数据映射结构，该结构通过把关键码映射的位置去寻找存放值的地方，
说起来可能感觉有点复杂，我想我举个例子你就会明白了，最典型的的例子就是字典，大家估计小学的时候也用过不少新华字典吧，
如果我想要获取“按”字详细信息，我肯定会去根据拼音an去查找 拼音索引（当然也可以是偏旁索引），我们首先去查an在字典的位置，
查了一下得到“安”，结果如下。这过程就是键码映射，在公式里面，就是通过key去查找f(key)。其中，按就是关键字（key），f（）就是字典索引，
也就是哈希函数，查到的页码4就是哈希值。
哈希冲突
哈希表的实现
如果为空，就直接插入。
插入数据时，解决冲突的办法：
cryptography-linux离线安装. 如果key相等，且在key所对应的位置上已有数据，就进行替换；
2.如果key不相等，就利用线性探测法，往后找一个位置，直到找到空的位置，再填入
'''


# python 实现哈希表

class HashTable:
    """
    哈希函数的构造
    解决冲突
    """

    def __init__(self, source):
        self.source = source
        self._index = []
        self._val = []
        self.table = []
        self._mod = 13

    def Output(self):
        print(self._index)
        print(self._val)

    def _create_table(self):
        """
        初始化哈希表
        哈希表长度最短为取余因子_mod,一般为源数据长度
        """
        if len(self.source) < self._mod:
            length = self._mod
        else:
            length = len(self.source)

        self._index = [i for i in range(length)]
        self._val = [None for i in range(length)]

    def _func_hash(self):
        """
        构建哈希函数
        """
        for sour in self.source:
            remainder = sour % self._mod
            if self._val[remainder] is None:
                self._val[remainder] = sour
            else:
                # 处理冲突
                rem = remainder
                while self._val[rem] is not None:
                    if (rem + 1 >= len(self._val)):
                        rem = -1
                    rem += 1
                self._val[rem] = sour
        self.table = list(zip(self._index, self._val))

    def get(self, num):
        """
        查找
        """
        rem = num % self._mod
        if self._val[rem] != num:
            while True:
                if (rem + 1 >= len(self._val)):
                    rem = 0
                if self._val[rem] == num:
                    break
                rem += 1
        return rem

    def run(self):
        self._create_table()
        self._func_hash()
        self.Output()


if __name__ == '__main__':
    test = [12, 15, 17, 21, 22, 25, 13, 0]
    h = HashTable(test)
    h.run()
    print(h.table)
    h.get(12)

