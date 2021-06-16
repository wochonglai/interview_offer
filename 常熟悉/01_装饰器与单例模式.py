# -*- coding:utf-8 -*-
'''
单例模式
'''

'''
cryptography-linux离线安装. 使用模块
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


'''
装饰器
'''
def a(func):
    def wrapper(*args,**kwargs):
        print('do something')
        func(*args,**kwargs)
    return wrapper

# 带参数的函数装饰器
def say_hello(contry):
    def wrapper(func):
        def deco(*args, **kwargs):
            if contry == "china":
                print("你好!")
            elif contry == "america":
                print('hello.')
            else:
                return

            # 真正执行函数的地方
            func(*args, **kwargs)
        return deco
    return wrapper

# 高阶用法：不带参数的类装饰器
class logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("[INFO]: the function {func}() is running..."\
            .format(func=self.func.__name__))
        return self.func(*args, **kwargs)

@logger
def say(something):
    print("say {}!".format(something))

say("hello")


# 高阶用法：带参数的类装饰器
class logger(object):
    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func): # 接受函数
        def wrapper(*args, **kwargs):
            print("[{level}]: the function {func}() is running..."\
                .format(level=self.level, func=func.__name__))
            func(*args, **kwargs)
        return wrapper  #返回函数

@logger(level='WARNING')
def say(something):
    print("say {}!".format(something))

say("hello")