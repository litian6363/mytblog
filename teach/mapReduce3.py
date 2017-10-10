#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

def str2float(s):
    le=0
    for n in s:
        if n=='.':
            break
        le+=1
#循环获得小数点的位置

    d={'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    z,f=0,0
#定义参数

    def zj(a,b):
        if isinstance(a,str):
            a=d[a]
        return a*10+d[b]
    z=reduce(zj,s[:le])
#转换整数

    def fj(a,b):
        if isinstance(a,str):
            a=d[a]
        return a*10+d[b]
    f=reduce(zj,s[le+1:])
    f=f/10**len(s[le+1:])
#转换小数并除以小数位数    

    return z+f
#整数与小数相加


print('str2float(\'123.456\') =', str2float('99587.123'))