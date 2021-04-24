'''
1.算法思想
基数排序（radix sort）属于“分配式排序”（distribution sort），又称“桶子法”（bucket sort）或bin sort，顾名思义，它是透过键值的部份资讯，
将要排序的元素分配至某些“桶”中，藉以达到排序的作用，基数排序法是属于稳定性的排序，其时间复杂度为O (nlog(r)m)，其中r为所采取的基数，
而m为堆数，在某些时候，基数排序法的效率高于其它的稳定性排序法。
2.代码实现
'''

# 2.1由桶排序改造，从最低位到最高位依次桶排序，最后输出最后排好的列表。
def RadixSort(list,d):
    for k in range(d):#d轮排序
        # 每一轮生成10个列表
        s=[[] for i in range(10)]#因为每一位数字都是0~9，故建立10个桶
        for i in list:
            # 按第k位放入到桶中
            s[i//(10**k)%10].append(i)
        # 按当前桶的顺序重排列表
        list=[j for i in s for j in i]
    return list

# 2.2简单实现
from random import randint
def radix_sort():
  A = [randint(1, 99999999) for _ in range(9999)]
  for k in range(8):
    S = [ [] for _ in range(10)]
    for j in A:
      S[j / (10 ** k) % 10].append(j)
    A = [a for b in S for a in b]
  for i in A:
    print(i)