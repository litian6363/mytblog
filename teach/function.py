#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

def quadratic(a, b, c):

    if not isinstance(a,(int,float)) and isinstance(b,(int,float)) and isinstance(c,(int,float)):
        raise TypeError('bad operand type!')
    if b*b-4*a*c<0:
        return '无实数根'
    elif b*b-4*a*c==0:
        return -b/2*a
    elif b*b-4*a*c>0:
        return '有两个结果 %f and %f' % ((-b-math.sqrt(b*b-4*a*c))/(2*a),(-b+math.sqrt(b*b-4*a*c))/(2*a))
# 测试:
print(quadratic(2, 3, 1)) # => (-0.5, -1.0)
print(quadratic(1, 3, -4)) # => (1.0, -4.0)