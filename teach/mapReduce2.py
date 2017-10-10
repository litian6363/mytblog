#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

def prod(L):
    def x(x1,x2):
       return x1*x2
    return reduce(x,L)


print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))