#!usr/bin/env python3
# -*- coding: utf-8 -*-


# 先序遍历，先根节点，然后左右
def preorder(tree):
    if tree:
        print(tree.get_root_value())
        preorder(tree.get_left_child())
        preorder(tree.get_right_child())
