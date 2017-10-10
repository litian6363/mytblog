#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def lower(list):
    return list.lower()

def normalize(name):
    l1=list(name)
    l2=list(map(lower,l1))
    l2[0]=l2[0].upper()
    return ''.join(l2)
    
    

# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)