#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def fact(n):
    '''
    >>> fact(2)
    2
    >>> fact(10)
    90
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n - 1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()