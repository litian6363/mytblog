#!/usr/bin/env python3
# -*- coding: utf-8 -*-

l =[]
n=0

while n <=100:
    l.append(n)
    n=n+2

n=0
lh=[]

while n <=len(l)/2:
    lh.append(l[n])
    n=n+1
    
print(lh)