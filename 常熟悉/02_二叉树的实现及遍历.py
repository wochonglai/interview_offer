# -*- coding:utf-8 -*-
#coding=utf-8

class Node(object):
    """节点类"""
    def __init__(self, elem=-1, lchild=None, rchild=None):
        self.elem = elem  # 节点的值
        self.lchild = lchild
        self.rchild = rchild


class Tree(object):
    """树类"""
    def __init__(self):
        self.root = Node()  # (self.root是节点类Node的对象)
        self.myQueue = []

    def add(self, elem):
        """为树添加节点"""
        node = Node(elem) # node是节点类Node的对象，这里初始化给了一个值
        if self.root.elem == -1:  # 如果树是空的，则对根节点赋值，（self.root.elem就是对象调用实例实现属性）
            self.root = node
            self.myQueue.append(self.root)
        else:
            treeNode = self.myQueue[0]  # 此结点的子树还没有齐。
            if treeNode.lchild == None:
                treeNode.lchild = node
                self.myQueue.append(treeNode.lchild)  # (这个就是每次增加一个节点，就将它的左子树置为None)
            else:
                treeNode.rchild = node
                self.myQueue.append(treeNode.rchild) # (这个就是每次增加一个节点，就将它的右子树置为None)
                self.myQueue.pop(0)  # 如果该结点存在右子树，将此结点丢弃。


    def front_digui(self, root):
        """利用递归实现树的先序遍历"""
        if root == None:
            return
        print(root.elem)
        self.front_digui(root.lchild)
        self.front_digui(root.rchild)


    def middle_digui(self, root):
        """利用递归实现树的中序遍历"""
        if root == None:
            return
        self.middle_digui(root.lchild)
        print(root.elem)
        self.middle_digui(root.rchild)


    def later_digui(self, root):
        """利用递归实现树的后序遍历"""
        if root == None:
            return
        self.later_digui(root.lchild)
        self.later_digui(root.rchild)
        print(root.elem)


    def front_stack(self, root):
        """利用堆栈实现树的先序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:                     #从根节点开始，一直找它的左子树，（当为None时结束循环，前面讲过每次增加节点就将它的左右子树置为None，这个就用到了）
                print(node.elem)  # (node是节点类的对象，所以调用实例属性)
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()            #while结束表示当前节点node为空，即前一个节点没有左子树了
            node = node.rchild                  #开始查看它的右子树


    def middle_stack(self, root):
        """利用堆栈实现树的中序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:                     #从根节点开始，一直找它的左子树
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()            #while结束表示当前节点node为空，即前一个节点没有左子树了
            print(node.elem)
            node = node.rchild                  #开始查看它的右子树


    def later_stack(self, root):
        """利用堆栈实现树的后序遍历"""
        if root == None:
            return
        myStack1 = []
        myStack2 = []
        node = root
        myStack1.append(node)
        while myStack1:                   #这个while循环的功能是找出后序遍历的逆序，存在myStack2里面
            node = myStack1.pop()
            if node.lchild:
                myStack1.append(node.lchild)
            if node.rchild:
                myStack1.append(node.rchild)
            myStack2.append(node)
        while myStack2:                         #将myStack2中的元素出栈，即为后序遍历次序
            print(myStack2.pop().elem)


    def level_queue(self, root):
        """利用队列实现树的层次遍历"""
        if root == None:
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            print(node.elem)
            if node.lchild != None:
                myQueue.append(node.lchild)
            if node.rchild != None:
                myQueue.append(node.rchild)


# class Node(object):
#     def __init__(self, val=None):
#         self.val = val
#         self.left = None
#         self.right = None
#
#
# def printTree(root):
#     if not root:
#         return
#     print('Binary Tree:')
#     printInOrder(root, 0, 'H', 17)
#
#
# def printInOrder(root, height, preStr, length):
#     if not root:
#         return
#     printInOrder(root.right, height + 1, 'v', length)
#     string = preStr + str(root.val) + preStr
#     leftLen = (length - len(string)) // 2
#     rightLen = length - len(string) - leftLen
#     res = " " * leftLen + string + " " * rightLen
#     print(" " * height * length + res)
#     printInOrder(root.left, height + 1, '^', length)
#
#
# head = Node(1)
# head.left = Node(-222222222)
# head.right = Node(3)
# head.left.left = Node(523)
# head.right.left = Node(55555555)
# head.right.right = Node(66)
# head.left.left.right = Node(777)
# printTree(head)



if __name__ == '__main__':
    """主函数"""
    elems = range(10)           #生成十个数据作为树节点
    tree = Tree()          #新建一个树对象
    for elem in elems:
        tree.add(elem)           #逐个添加树的节点

    # print('队列实现层次遍历:')
    # tree.level_queue(tree.root)
    #
    # print('\n\n递归实现先序遍历:')
    # tree.front_digui(tree.root)
    # print('\n递归实现中序遍历:')
    # tree.middle_digui(tree.root)
    # print('\n递归实现后序遍历:')
    # tree.later_digui(tree.root)
    #
    # print('\n\n堆栈实现先序遍历:')
    # tree.front_stack(tree.root)
    # print('\n堆栈实现中序遍历:')
    # tree.middle_stack(tree.root)
    # print('\n堆栈实现后序遍历:')
    # tree.later_stack(tree.root)
