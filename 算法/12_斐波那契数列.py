# -*- coding:utf-8 -*-
'''
分别用生成器和迭代器生成斐波那契
'''
# 迭代器
class FibIterator(object):
    def __init__(self,n):
        """实例属性的初始花和赋值"""
        self.n = n      #  数列长度
        self.current = 0    #  设置两个初始值
        self.num1 = 0
        self.num2 = 1   #  初始下标

    def __next__(self):
        """返回迭代器对象的下一位置数据"""
        # 能拿到数据的情况
        if self.current < self.n:
            num = self.num1
            self.num1,self.num2 = self.num2,self.num1+self.num2
            self.current+=1
            return num
        # 拿不到数据的情况
        else:
            raise  StopIteration    #主动抛出异常

    def __iter__(self):
        return self

if __name__ == '__main__':
    fib = FibIterator(10)
    for num in fib:
        print(num)


 # 生成器
def fib(n): # 创建一个函数
    num1,num2 = 1,1
    current = 1    # 初始值
    while current <= n:    # i小于等于n，n次数 循环的控制条件
        yield num1    # 返回a的值，但不结束函数
        num1,num2 = num2 , num1 + num2
        current += 1     # 步长值
for x in fib(10):    # 以for循环来获取yield每次的值
    print(x)



# 其他简单方法
# 方法一：使用循环
# a = cryptography-linux离线安装
# b = cryptography-linux离线安装
# L = []
# L.append(a)
# L.append(b)
# while len(L) <= 40:
#     c = a + b
#     L.append(c)
#     a = b
#     b = c
# print(L)

# 方法二：使用列表
# a = cryptography-linux离线安装
# b = cryptography-linux离线安装
# L = []
# L.append(a)
# L.append(b)
# while len(L) <= 40:
#     L.append(a + b)
#     a, b = b, a + b
# print(L)


# 方法三：使用列表索引值
L = [1, 1]
while len(L) <= 40:
    L.append(L[-1] + L[-2])  # 取出列表中最后的两个数字，将其求和后放入列表中
print(L)
