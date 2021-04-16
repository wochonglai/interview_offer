# -*- coding:utf-8 -*-
'''
839. 相似字符串组
如果交换字符串 X 中的两个不同位置的字母，使得它和字符串 Y 相等，那么称 X 和 Y 两个字符串相似。如果这两个字符串本身是相等的，那它们也是相似的。
例如，"tars" 和 "rats" 是相似的 (交换 0 与 2 的位置)； "rats" 和 "arts" 也是相似的，但是 "star" 不与 "tars"，"rats"，或 "arts" 相似。
总之，它们通过相似性形成了两个关联组：{"tars", "rats", "arts"} 和 {"star"}。注意，"tars" 和 "arts" 是在同一组中，即使它们并不相似。形式上，对每个组而言，要确定一个单词在组中，只需要这个词和该组中至少一个单词相似。
给你一个字符串列表 strs。列表中的每个字符串都是 strs 中其它所有字符串的一个字母异位词。请问 strs 中有多少个相似字符串组

示例 1：

输入：strs = ["tars","rats","arts","star"]
输出：2
示例 2：

输入：strs = ["omv","ovm"]

备注：
      字母异位词（anagram），一种把某个字符串的字母的位置（顺序）加以改换所形成的新词。

解题思路
今天的题目的中文题意比较模糊，我看了很久才明白 相似字符串组 的含义。即相似字符串组中的每个字符串都有另外至少一个字符串和它相似。比如对于 {"tars", "rats", "arts"} 这个相似字符串组而言，相似关系是 "tars" <=> "rats" <=> "arts" 。

两个字符串相似的含义是能够通过交换两个字符的位置，得到另外一个字符串。判断两个字符串相似的时间的复杂度是 O(N)，因为把所有位置遍历一次，统计两个字符串的对应位置有多少不等即可。

明白了题意之后，做法也就呼之欲出了：把每个字符串当做图中的一个节点，如果两个字符串相似，那么它们之间就有一条边。图中的每个连通区域是一个相似字符串组。问：图中有多少个不连通的区域？

很显然，图的连通性问题可以用「并查集」去做。然后套「并查集」的模板就可以了。

这也是我之前说的：“在明白题目考察什么之后，剩下的就是套模板”。

和今天题目非常类似的题目是「1579. 保证图可完全遍历」，我前几天的文章已经详细分析过了，两者都是考察图中有多少个连通区域，都是直接使用并查集模板。

代码
每个字符串都是一个节点，我们需要分析每两个节点之间是否相似，如果相似就添加一条边，使用并查集，看最终有多少个连通区域。

代码思路：

两重 for 循环，实现对节点之间两两组合，判断两个节点是否相似；
判断相似的方法是：两个字符串的对应位置中只有 0 个或者 2 个不同；
如果两个字符串相似则使用并查集，将此两个节点之间连通上一条边；
统计最终并查集中有多少个不同的连通区域，即为所求。
复杂度分析：

时间复杂度：O(N ^ 2 * M)O(N
2
 ∗M)，其中 NN 是数组的长度，MM 是单个字符串的长度。忽略了并查集的时间复杂度。这样一算，计算量大概 10 ^ 810
8
 ，已经到达了力扣的计算量上限，刚好这题能过了。

空间复杂度：O(N)O(N)，并查集需要一个长度为 NN 的数组。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/similar-string-groups
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''

class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        n=len(strs)
        m=len(strs[0])
        u=UnionFind(n)
        for i in range(n):
            for j in range(i + 1, n):
                count = 0
                for k in range(m):
                    if strs[i][k] != strs[j][k]:
                        count += 1
                        if count > 2:
                            break
                if count in {0, 2}:
                    u.union(i, j)
        return u.count


class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.count = n

    def find(self, x):
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            self.parent[x] = y
            self.count -= 1