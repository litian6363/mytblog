#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fv(name,age,**other):
    
    print(name,age,other)


t1={'sex' :'man' ,'hobby' :'python'} 

fv('tian','20',**t1)