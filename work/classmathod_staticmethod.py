# -*- coding:utf-8 -*-

class Door(object):
    a = 1

    def __init__(self, num, status):
        self.num = num
        self.status = status

    def open(self):
        self.var = 0
        self.status = 'open'

    def close(self):
        self.status = 'closed'

    def __test(self):
        print('__test')

    @classmethod
    def test(cls):
        print("class test")
        # 不需要self参数，但第一个参数需要是表示自身类的cls参数。
        print(cls.a)

    @staticmethod
    def test2():
        print("static test2")
        # 不需要自身对象参数，直接使用类名+类变量调用
        print(Door.a)


Door.test()
d1 = Door(1, "closed")
d1.test()
# 通过类名调用和通过实例调用
d2 = Door(2, "closed")
Door.test2()
d2.test2()
