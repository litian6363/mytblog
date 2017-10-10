#!/usr/bin/env python3
# -*- coding: utf-8 -*-

L1 = ['Hello', 'World', 18, 'Apple', None]

L2 = [m.lower() for m in L1 if isinstance(m,str)]

# ÆÚ´ýÊä³ö: ['hello', 'world', 'apple']
print(L2)