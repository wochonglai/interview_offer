# -*- coding:utf-8 -*-
'''
用于生成自定义的colormap
'''
import matplotlib.colors as col
import matplotlib.cm as cm


# example 2: use the "fromList() method
startcolor = '#ff0000'   #红色，读者可以自行修改
midcolor = '#00ff00'     #绿色，读者可以自行修改
endcolor = '#0000ff'          #蓝色，读者可以自行修改
cmap2 = col.LinearSegmentedColormap.from_list('own2',[startcolor,midcolor,endcolor])
# extra arguments are N=256, gamma=1.0
cm.register_cmap(cmap=cmap2)
# we can skip name here as it was already defined

'''
当register_cmap执行完毕后，调用该color map 的名称 'own2'，即可。
cm.get_cmap('own2')
就获得了文章开头的红-绿-蓝有过渡的颜色映射。函数自动使用插值计算0-1之间的颜色。
'''