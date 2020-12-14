# -*- coding:utf-8 -*-
'''
二分查找非常简单，是建立在列表有序的情况下，利用二分法不断逼近目标值的。
'''
def binary_search(arr,target):
    left=0
    right=len(arr)-1
    while left<=right:
        mid=(right-left)//2
        if target>arr[mid]:
            left=mid+1  # 如果比目标值比中位值还要大，调整右边界指针
        elif target<arr[mid]:
            right=mid-1 # 如果比目标值比中位值要小，调整左边界指针
        else:
            return mid
    return -1
