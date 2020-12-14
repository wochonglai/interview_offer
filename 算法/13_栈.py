# -*- coding:utf-8 -*-
'''
也称下压栈，堆栈，是仅允许在表尾进行插入和删除操作的线性表,
特点：先进后出 后进先出
'''
class Stack(object):
    def __init__(self):
        self.stack=[]

    def push(self,item):
        """push(item)添加一个新的元素item到栈顶"""
        self.stack.append(item)

    def pop(self):
        """pop()弹出栈顶元素"""
        if self.stack==[]:
            return None
        else:
            self.stack.pop()

    def peek(self):
        """peek()返回栈顶元素"""
        if self.stack==[]:
            return None
        else:
            return self.stack[-1]

    def isEmpty(self):
        """is_empty()判断栈是否为空"""
        return self.stack == []

    def size(self):
        """size()返回栈的元素个数"""
        return len(self.stack)

if __name__ == '__main__':
    stack = Stack()
    stack.push(1)
    stack.pop()
    print(stack.peek())
    print(stack.isEmpty())
    print(stack.size())