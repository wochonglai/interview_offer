'''
归并排序是分治法的典型应用。分治法（Divide-and-Conquer）：将原问题划分成 n 个规模较小而结构与原问题相似的子问题；递归地解决这些问题，然后再合并其结果，就得到原问题的解，分解后的数列很像一个二叉树。
具体实现步骤：
使用递归将源数列使用二分法分成多个子列
申请空间将两个子列排序合并然后返回
将所有子列一步一步合并最后完成排序
注：先分解再归并
'''
def merge_sort(arr):
    #归并排序
    if len(arr) == 1:
        return arr
    # 使用二分法将数列分两个
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    # 使用递归运算
    return marge(merge_sort(left), merge_sort(right))


def marge(left, right):
    #排序合并两个数列
    result = []
    # 两个数列都有值
    while len(left) > 0 and len(right) > 0:
        # 左右两个数列第一个最小放前面
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    # 只有一个数列中还有值，直接添加
    result += left
    result += right
    return result
