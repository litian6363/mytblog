#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通过cython，用py文件生成C文件，然后根据对应系统的C编辑器，生成动态链接库文件，最后删除C文件

用法：
将该文件放在需要编译的文件夹或上层文件夹下，运行

依赖：
pip install cython

window ps:
需要下载需要安装对应python版本的Microsoft Visual C / C++
参考：http://matthew-brett.github.io/pydagogue/python_msvc.html
"""

__author__ = 'LiTian'

import os
import shutil
from distutils.core import setup
from Cython.Build import cythonize


def get_file_path(file_type, exclude=()):
    """获取当前文件所在目录或子目录下的file_type后序的文件路径，排除exclude"""
    path_list = []
    for root, dirs, files in os.walk(os.curdir):
        for file in files:
            if file.endswith(file_type) and file not in exclude:
                path_list.append(os.path.join(root, file))
    return path_list


if __name__ == '__main__':
    # 生成动态链接库
    try:
        py_list = get_file_path('.py', (__file__, '__init__.py'))
        setup(
            ext_modules=cythonize(py_list), script_args=['build_ext', '--inplace']
        )
    except Exception as e:
        print('Error: %s' % e)
    finally:
        # 删除c语言文件
        dele_list = get_file_path('.c')
        for file in dele_list:
            os.remove(file)
    shutil.move(os.path.join(os.curdir, os.path.basename(os.path.abspath('.'))), '.abs')
