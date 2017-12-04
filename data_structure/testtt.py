#!usr/bin/env python3
# -*- coding: utf-8 -*-

from mytblog.data_structure.simulation import BinaryHeap

if __name__ == '__main__':
    a = BinaryHeap()
    a.build_heap([18, 19, 5, 9, 11, 21, 33, 17, 27, 14, 19])
    a.insert(4)
    a.insert(13)
    for i in range(0, 7):
        print(a.del_min())
