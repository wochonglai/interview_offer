# -*- coding:utf-8 -*-
'''
单例模式
'''

'''
1. 使用模块
其实,python的模块就是天然的单例模式,因为模块在第一次导入的时候,会生成.pyc文件,当第二次导入的时候,就会直接加载.pyc文件,而不是再次执行模块
代码.如果我们把相关的函数和数据定义在一个模块中,就可以获得一个单例对象了.
'''
# 2
class Sun(object):
    __instance=None #定义一个类属性做判断
    def __new__(cls):
        if cls.__instance==None:
            #如果__instance为空证明是第一次创建实例
            #通过父类的__new__(cls)创建实例
            cls.__instance==object.__new__(cls)
            return cls.__instance
        else:
            #返回上一个对象的引用
            return cls.__instance



