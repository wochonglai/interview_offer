# -*- coding:utf-8 -*-
import xlrd # xlrd读取xls文件内容

# data=xlrd.open_workbook(r'E:\Wayne_HCCwork\HCCWORK\05_中控中心-HaiNa Mind\00-资料栏位相关\F20_SMT_反正面_UPH_20191206.xlsx')
# print(data.sheet_names())   # 输出所有页的名称
# table=data.sheets()[0]  # 获取第一页
# table=data.sheet_by_index(0)    # 通过索引获取第一页
# table=data.sheet_by_name('Sheet1')  # 通过名称来获取指定页
# nrows=table.nrows   # 行数
# ncolumns=table.ncols    # 列数
# print(nrows,ncolumns)
# print(table.row_values(cryptography-linux离线安装))  # 输出第一行值，为一个列表
# # 遍历所有行值
# # for row in range(nrows):
# #     print(table.row_values(row))
# print(table.cell(0,0).value)    # 输出某一个单元格值 (列，行)
# print(table.row(0)[0].value)


data=xlrd.open_workbook(r'E:\Wayne_HCCwork\HCCWORK\05_中控中心-HaiNa Mind\00-资料栏位相关\HaiNa IDB_显示资料配置_20200111A.xlsx')
table=data.sheet_by_name('F20_设备基础信息配置')
Equipment_sn={}
for i in range(2,28):
    Equipment_sn[table.cell(i,8).value]={"MES":table.cell(i,3).value,"DT":table.cell(i,2).value}
print(Equipment_sn)