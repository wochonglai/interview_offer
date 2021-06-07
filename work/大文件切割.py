# -*- coding:utf-8 -*-

from datetime import datetime


def file_split(filesource,target_dir,split_lines):
    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []

    print("开始。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(filesource, 'r',encoding='utf8') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == split_lines:
                with open(target_dir + "_" + str(name) + ".txt", 'a') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于*行的
    with open(target_dir + "_" + str(name) + ".txt", 'w+') as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    file_source = r'E:\data_bak01\demo_data\HCCDemoData_F20.20200704-20200706.txt'
    target_dir = r'E:\data_bak01\demo_data\HCCDemoData_F20.20200704-20200706-Group C\HCCDemoData_F20.20200704-20200706'
    split_lines=10000   # 以多少行切割
    file_split(file_source,target_dir,split_lines)
