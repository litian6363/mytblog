#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

def log(text=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            print('begin %s %s():'%(text,func.__name__))
            aa = func(*arg,**kw)
            print('end %s %s():'%(text,func.__name__))
            return aa
        return wrapper
    return decorator



@log()
def test1():
    print('20170321')
    
    
test1()