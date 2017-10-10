#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def triangles():
    l = [1]
    while True:
        yield l
        l.append(0)
        l = [l[n]+l[n-1] for n in range(len(l))]
        
        

n=0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break
        
