#!/usr/bin/env python3
# -*- coding: utf-8 -*-


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_score(t):
    t1=[]
    for ob in t:
        if isinstance(ob,(int,float)):
            t1.append(ob)
    return t1

L2 = sorted(L,key=by_score,reverse=True)

print(L2)