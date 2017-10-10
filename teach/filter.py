#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import reduce


def is_palindrome(n):
    s,r,l=list(str(n)),list(str(n)),0
    while l<len(s)//2:
        s[l]=r[-1-l]
        s[-1-l]=r[l]
        l=l+1
    
    def lcn(x,y):
        return int(x)*10+int(y)
    n1 = reduce(lcn,s)
    
    return n1==n
        

# 测试:
output = filter(is_palindrome, range(1, 10000))
print(list(output))