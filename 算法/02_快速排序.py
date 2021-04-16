# -*- coding:utf-8 -*-
'''
快速排序（Quick Sort）
快速排序的基本思想：通过一趟排序将待排记录分隔成独立的两部分，其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序。

6.1 算法描述
快速排序使用分治法来把一个串（list）分为两个子串（sub-lists）。具体算法描述如下：

从数列中挑出一个元素，称为 “基准”（pivot）；
重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作；
递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。
'''
def quick_sort(arr):
    if len(arr)<2:
        return arr
    else:
        # 递归条件
        pivot=arr[0]
        # 由所有小于基准值的元素组成的子数组
        less = [i for i in arr[1:] if i <= pivot]
        # 由所有大于基准值的元素组成的子数组
        greater = [i for i in arr[1:] if i > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)


dict

# 思路二
import random


class Solution(object):
    """
    快排
    时间复杂度为O(nlogn),最差情况为O(n2)
    空间复杂度为O(logn)
    """

    def partition(self, li: list, left, right):
        tmp = li[left]

        while left < right:
            while left < right and li[right] >= tmp:
                right -= 1
            li[left] = li[right]

            while left < right and li[left] <= tmp:
                left += 1
            li[right] = li[left]
        li[left] = tmp
        return left

    def quick_sort(self, li, left, right):
        if left < right:
            mid = self.partition(li, left, right)
            self.quick_sort(li, left, mid - 1)
            self.quick_sort(li, mid + 1, right)




li = list(range(100))
random.shuffle(li)
print(li)
solution = Solution()
print(solution.quick_sort(li, 0, len(li) - 1))
print(li)