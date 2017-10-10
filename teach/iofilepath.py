#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def myinput() :
    key = input('请输入需要搜索的关键词,退出请输入 exit : ')
    if key=='exit':
        os._exit(0)
    else : 
        mysearch(key,'.')

def mysearch(key,mypath):
    for x in os.listdir(mypath):
        if os.path.isfile(os.path.join(mypath,x)) and key in x:
            print(os.path.join(mypath,x))
        elif os.path.isdir(x):
            mysearch(key,os.path.join(mypath,x))
    
myinput()