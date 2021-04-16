# -*- coding:utf-8 -*-
# Dynamic Programming
'''
1、https://www.bilibili.com/video/BV12W411v7rd/?spm_id_from=autoNext
给定一个列表，从中选择两两不相邻的n个数字，使其和最大.
Optimize
v.	使最优化; 充分利用;
'''
arr=[1,2,4,1,7,8,3]

# 常规递归算法会使时间复杂度达到2的n次方
def rec_opt(arr,i):
    if i==0:
        return arr[0]
    elif i==1:
        return max(arr[0],arr[1])
    else:
        return max(rec_opt(arr,i-2)+arr[i],rec_opt(arr,i-1))

print(rec_opt(arr,len(arr)-1))

# 动态规划，时间复杂度为n
import numpy as np
def dp_opt(arr,i):
    opt=np.zeros(len(arr))
    opt[0]=arr[0]
    opt[1]=max(arr[0],arr[1])
    for i in range(2,len(arr)):
        A=opt[i-2]+arr[i]   # 选第i个
        B=opt[i-1]          # 不选第i个
        opt[i]=max(A,B)
    return opt[len(arr)-1]
print(dp_opt(arr,len(arr)-1))

'''
类似的从一个列表中选几个数字，使和为某一个数，存在输出True，不存在输出False
都是选与不选，找递归出口
'''
arr=[1,2,4,1,7,8,3]
s=9
# 递归
def rec_subset(arr,i,s):
    if s==0:
        return True
    elif i==0:
        return arr[0]==s
    elif arr[i]>s:
        return rec_subset(arr,i-1,s)
    else:
        A=rec_subset(arr,i-1,s-arr[i])
        B=rec_subset(arr,i-1,s)
        return A or B

print(rec_subset(arr,len(arr)-1,14))

# 非递归动态规划
import numpy as np
def dp_subset(arr,s):
    subset=np.zeros((len(arr),s+1),dtype=bool)
    subset[:,0]=True    # 第一列
    subset[0,:]=False # 第一行
    subset[0,arr[0]]=True
    for i in range(1,len(arr)):
        for s in range(1,s+1):
            if arr[i]>s:
                subset[i,s]=subset[i-1,s]
            else:
                A = rec_subset(i - 1, s - arr[i])
                B = rec_subset(i - 1, s)
                subset[i,s]=A or B
    r,c=subset.shape
    return subset[r-1,c-1]

print(dp_subset(arr,len(arr)-1,14))

