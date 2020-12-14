# -*- coding:utf-8 -*-
'''
堆排序（Heap Sort）
堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。堆积是一个近似完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。

算法描述
将初始待排序关键字序列(R1,R2….Rn)构建成大顶堆，此堆为初始的无序区；
将堆顶元素R[1]与最后一个元素R[n]交换，此时得到新的无序区(R1,R2,……Rn-1)和新的有序区(Rn),且满足R[1,2…n-1]<=R[n]；
由于交换后新的堆顶R[1]可能违反堆的性质，因此需要对当前无序区(R1,R2,……Rn-1)调整为新堆，然后再次将R[1]与无序区最后一个元素交换，得到新的无序区(R1,R2….Rn-2)和新的有序区(Rn-1,Rn)。不断重复此过程直到有序区的元素个数为n-1，则整个排序过程完成

算法思想

堆分为最大堆和最小堆，是完全二叉树。堆排序就是把堆顶的最大数取出，将剩余的堆继续调整为最大堆,具体过程在第二块有介绍，以递归实现 ，
剩余部分调整为最大堆后,再次将堆顶的最大数取出，再将剩余部分调整为最大堆,这个过程持续到剩余数只有一个时结束。
'''
import time,random
def sift_down(arr, node, end):
    root = node
    #print(root,2*root+1,end)
    while True:
        # 从root开始对最大堆调整
        child = 2 * root +1  #left child
        if child  > end:
            #print('break',)
            break
        print("v:",root,arr[root],child,arr[child])
        print(arr)
        # 找出两个child中交大的一个
        if child + 1 <= end and arr[child] < arr[child + 1]: #如果左边小于右边
            child += 1 #设置右边为大
        if arr[root] < arr[child]:
            # 最大堆小于较大的child, 交换顺序
            tmp = arr[root]
            arr[root] = arr[child]
            arr[child]= tmp
            # 正在调整的节点设置为root
            #print("less1:", arr[root],arr[child],root,child)
            root = child #
            #[3, 4, 7, 8, 9, 11, 13, 15, 16, 21, 22, 29]
            #print("less2:", arr[root],arr[child],root,child)
        else:
            # 无需调整的时候, 退出
            break
    #print(arr)
    print('-------------')

def heap_sort(arr):
    # 从最后一个有子节点的孩子还是调整最大堆
    first = len(arr) // 2 -1
    for i in range(first, -1, -1):
        sift_down(arr, i, len(arr) - 1)
    #[29, 22, 16, 9, 15, 21, 3, 13, 8, 7, 4, 11]
    print('--------end---',arr)
    # 将最大的放到堆的最后一个, 堆-1, 继续调整排序
    for end in range(len(arr) -1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(arr, 0, end - 1)
        #print(arr)
