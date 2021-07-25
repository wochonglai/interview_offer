#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup-sample.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/7/25 21:01   wayne      1.0         None
'''

'''
最近, 作者遇到一个需求, 需要把Python的工程部署到别的集群, 但是又要保证Python代码的安全性. 于是上网搜索, 搜到几个解决方案, 但是都不是符合需求. 综合搜到的几个解决方案, 最终作者采用了编译成so动态库的方式发布.

首先说一下搜到到几个解决方案, 以及它们的优缺点

编译成pyc发布
优点: 操作简单
缺点: 可以被反编译
cx_freeze
优点: 可以通过freeze命令直接把一个项目所有的依赖生成一个二进制, 所以部署到新的环境时, 十分方便
缺点: freeze命令如果工程项目很大的话, 速度非常慢, 而且其生成的Python代码其实也是pyc, 可以被反编译
pyminifier
优点: 通过代码混淆的方式保护代码的安全
缺点: 貌似, 只对单个文件的混淆其作用, 如果是一个工程项目就不好使了
cython编译成动态库
优点: 可以将代码编译成.so动态库, 起到代码保护的作用
缺点: 编译速度太慢了
综合以上几个优缺点, 作者最终选择了通过cython编译成动态库的方式, 来达到保护Python代码的目的, cython官方文档

说下具体的做法和原理:
cython首先会把python代码翻译成C语言代码, 然后cython在将其编译成.so动态库, 最后, 在编译好的build/lib.linux-x86_64-2.7(不同的平台和python版本这个目录是不一样, 作者的是linux平台, Python2.7版本)文件夹中, 直接引用即可.
但是这里有一个坑, 如果你编译的是一个Python的库, 那么你的build/lib.linux-x86_64-2.7中的库文件中, 每个库里必须有一个__init__.py文件, 所以, 下面的代码会首先进行一个把一个空的__init__.py文件拷贝到对应的库中的操作, 然后搜寻所有的.py文件, 将其编译成动态库, 然后把所有的非.py文件, 移动到原目录对应的位置. 下面是对应的转换的setup.py文件和例子

https://www.cnblogs.com/spxcds/p/10204419.html
'''
import os
import sys
import shutil
import numpy
import tempfile

from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

import platform

build_root_dir = 'build/lib.' + platform.system().lower() + '-' + platform.machine() + '-' + str(
    sys.version_info.major) + '.' + str(sys.version_info.minor)

print(build_root_dir)

extensions = []
ignore_folders = ['build', 'test', 'tests']
conf_folders = ['conf']


def get_root_path(root):
    if os.path.dirname(root) in ['', '.']:
        return os.path.basename(root)
    else:
        return get_root_path(os.path.dirname(root))


def copy_file(src, dest):
    if os.path.exists(dest):
        return

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copyfile(src, dest)


def touch_init_file():
    init_file_name = os.path.join(tempfile.mkdtemp(), '__init__.py')
    with open(init_file_name, 'w'):
        pass
    return init_file_name


init_file = touch_init_file()
print(init_file)


def compose_extensions(root='.'):
    for file_ in os.listdir(root):
        abs_file = os.path.join(root, file_)

        if os.path.isfile(abs_file):
            if abs_file.endswith('.py'):
                extensions.append(Extension(get_root_path(abs_file) + '.*', [abs_file]))
            elif abs_file.endswith('.c') or abs_file.endswith('.pyc'):
                continue
            else:
                copy_file(abs_file, os.path.join(build_root_dir, abs_file))
            if abs_file.endswith('__init__.py'):
                copy_file(init_file, os.path.join(build_root_dir, abs_file))

        else:
            if os.path.basename(abs_file) in ignore_folders:
                continue
            if os.path.basename(abs_file) in conf_folders:
                copy_file(abs_file, os.path.join(build_root_dir, abs_file))
            compose_extensions(abs_file)


compose_extensions()
os.remove(init_file)

setup(
    name='my_project',
    version='1.0',
    ext_modules=cythonize(
        extensions,
        nthreads=16,
        compiler_directives=dict(always_allow_keywords=True),
        include_path=[numpy.get_include()]),
    cmdclass=dict(build_ext=build_ext))

# python setup.py build_ext


'''
下面是一个例子

目录结构是这样子的
.
├── main.py
├── mypkg
│   ├── foo.py
│   ├── __init__.py
│   └── t
│       ├── __init__.py
│       └── t.py
└── setup.py

然后运行命令python setup.py build_ext 即可看到新的目录结构

├── build
│   ├── lib.linux-x86_64-2.7
│   │   ├── main.so
│   │   ├── mypkg
│   │   │   ├── foo.so
│   │   │   ├── __init__.py
│   │   │   ├── __init__.so
│   │   │   └── t
│   │   │       ├── __init__.py
│   │   │       ├── __init__.so
│   │   │       └── t.so
│   │   └── setup.so
│   └── temp.linux-x86_64-2.7
│       ├── main.o
│       ├── mypkg
│       │   ├── foo.o
│       │   ├── __init__.o
│       │   └── t
│       │       ├── __init__.o
│       │       └── t.o
│       └── setup.o
├── main.c
├── main.py
├── mypkg
│   ├── foo.c
│   ├── foo.py
│   ├── __init__.c
│   ├── __init__.py
│   └── t
│       ├── __init__.c
│       ├── __init__.py
│       ├── t.c
│       └── t.py
├── setup.c
└── setup.py

然后, 将main.py拷贝到build/lib.linux-x86_64-2.7 直接就可以运行了
.
├── main.py
├── main.so
├── mypkg
│   ├── foo.so
│   ├── __init__.py
│   ├── __init__.so
│   └── t
│       ├── __init__.py
│       ├── __init__.so
│       └── t.so
└── setup.so

$ cat main.py

from mypkg.foo import hello
from mypkg import fun1
from mypkg.t.t import t

if __name__ == '__main__':
    hello()
    fun1()
    t()

$ python main.py
this is in hello
this is in fun1
this is in t
'''