#!usr/bin/env python3
# -*- coding: utf-8 -*-


# 先序遍历，先根节点，然后左右
def preorder(tree):
    if tree:
        print(tree.get_root_value())
        preorder(tree.get_left_child())
        preorder(tree.get_right_child())


# 后序遍历，先左右，再根节点
def postorder(tree):
    if tree is not None:
        postorder(tree.get_left_child())
        postorder(tree.get_left_child())
        print(tree.get_root_value())


# 中序遍历，先左节点，然后根节点。最后右节点
def inorder(tree):
    if tree is not None:
        inorder(tree.get_left_child())
        print(tree.get_root_value())
        inorder(tree.get_right_child())
