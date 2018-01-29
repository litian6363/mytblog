#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

myPath = sys.path
for i in myPath:
    print(i)
from test1 import f
print(f(2))