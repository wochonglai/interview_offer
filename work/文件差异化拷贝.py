#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
在项目中，经常要更新文件，在更新之前首先要备份源文件，所以就用到了这个脚本（来自于Python自动化运维这本书），总共有以下几个步骤：


获取要进行比较的两个目录，进行差异比较，把源目录特有的文件或目录、以及和备份目录不同的文件或目录保存到列表中，并且判断目录下面是否还有目录，递归进行保存这些差异文件。
将差异文件列表中文件或目录的路径换成对应的备份路径，进行判断，如果备份路径不存在，就创建目录。
继续对比源目录和新创建的备份目录中的差异文件，把源路径换成备份目录的路径。
然后遍历复制源目录文件到备份目录。

---------------------
不错，谢谢了，re.sub在进行路径替换的时候会有问题，修改成destination_dir = item.replace(r''+dir1, r''+dir2)后就好了
第三步加上判断防止重复操作 destination_files.append(destination_dir) 改为 if destination_dir not in destination_files: destination_files.append(destination_dir)

本文来自 乱弹世界 的CSDN博客 ，全文地址请点击：https://blog.csdn.net/linxi7/article/details/60757495?utm_source=copy
'''
import os, sys
import filecmp
import re
import shutil

holderlist = []

##对应第一个步骤
def compare_me(dir1, dir2):
    dircomp = filecmp.dircmp(dir1, dir2)
    only_in_one = dircomp.left_only
    diff_in_one = dircomp.diff_files
    dirpath = os.path.abspath(dir1)

    [ holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in only_in_one ]
    [ holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in diff_in_one ]
    if len(dircomp.common_dirs) > 0:
        for item in dircomp.common_dirs:
            compare_me(os.path.abspath(os.path.join(dir1, item)), os.path.abspath(os.path.join(dir2, item)))
    return holderlist

##对应第二个步骤
def main():
    if len(sys.argv) > 2:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
    else:
        print("Usage: ", sys.argv[0], "datadir backupdir")
        sys.exit()

    source_files = compare_me(dir1, dir2)
    dir1 = os.path.abspath(dir1)
    if not dir2.endswith('/'):
        dir2 = dir2 + '/'
    dir2 = os.path.abspath(dir2)
    destination_files = []
    createdir_bool = False

    for item in source_files:
        destination_dir = re.sub(dir1, dir2, item)
        destination_files.append(destination_dir)
        if os.path.isdir(item):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                createdir_bool = True

     ##对应第三个步骤    
    if createdir_bool:
        destination_files = []
        source_files = []
        source_files = compare_me(dir1, dir2)
        for item in source_files:
            destination_dir = re.sub(dir1, dir2, item)
            destination_files.append(destination_dir)

    ##对应第四个步骤
    print("update item: ")
    print(source_files)
    copy_pair = zip(source_files, destination_files)
    print("copy_pair is %s" % copy_pair)
    for item in copy_pair:
        print("item is %s,  %s" % (item[0], item[1]))
        if os.path.isfile(item[0]):
            shutil.copyfile(item[0], item[1])

if __name__ == '__main__':
    main()