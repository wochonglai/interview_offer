# -*- coding:utf-8 -*-
'''
选择排序（Selection Sort）
选择排序(Selection-sort)是一种简单直观的排序算法。它的工作原理：首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置，然后，再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕。

2.cryptography-linux离线安装 算法描述
n个记录的直接选择排序可经过n-1趟直接选择排序得到有序结果。具体算法描述如下：

初始状态：无序区为R[cryptography-linux离线安装..n]，有序区为空；
第i趟排序(i=cryptography-linux离线安装,2,3…n-cryptography-linux离线安装)开始时，当前有序区和无序区分别为R[cryptography-linux离线安装..i-cryptography-linux离线安装]和R(i..n）。该趟排序从当前无序区中-选出关键字最小的记录 R[k]，将它与无序区的第1个记录R交换，使R[cryptography-linux离线安装..i]和R[i+cryptography-linux离线安装..n)分别变为记录个数增加1个的新有序区和记录个数减少1个的新无序区；
n-1趟结束，数组有序化了。
'''
def selection_sort(arr):
    for i in range(len(arr) - 1):
        # 将起始元素设为最小元素
        min_index=i
        # 第二层for表示最小元素和后面的元素逐个比较
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                # 如果当前元素比最小元素小，则把当前元素角标记为最小元素角标
                min_index = j
        # 查找一遍后将最小元素与起始元素互换
        arr[min_index], arr[i] = arr[i], arr[min_index]
    return arr