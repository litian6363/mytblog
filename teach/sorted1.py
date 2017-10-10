#!/usr/bin/env python3
# -*- coding: utf-8 -*-


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
    t1=[]
    for ob in t :
        if isinstance(ob,str):
            t1.append(ob)
    return t1

    
    
L2 = sorted(L, key=by_name)
print(L2)