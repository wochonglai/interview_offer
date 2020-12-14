# -*- coding:utf-8 -*-
'''
队列：是只允许在一端进行插入操作，而在另一端进行删除操作的线性表。
特点：先进先出 后进后出
'''
class Queue(object):
    def __init__(self):
        """实例属性的初始化和赋值创建一个空的队列"""
        self.queue = []

    def enqueue(self,item):
        """往队列中添加一个item元素"""
        self.queue.append(item)

    def is_empty(self):
        """判断一个队列是否为空"""
        return self.queue==[]

    def dequeue(self):
        """从队列头部删除一个元素"""
        if self.queue==[]:
            return None
        else:
            return  self.queue.pop(0)

    def size(self):
        """返回队列大小"""
        return  len(self.queue)
if __name__ == '__main__':
    q=Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    print(q.is_empty())
    print("长度为：",q.size())
    print(q.dequeue())
