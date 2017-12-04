#!usr/bin/env python3
# -*- coding: utf-8 -*-

# 怎样根据一个全括号数学表达式((7+3)*(5-2))来建立其对应的解析树
# 怎样计算解析树中数学表达式的值
# 怎样根据一个解析树还原数学表达式

from mytblog.data_structure.simulation import Stack, BinaryTree
import operator


# 将算式去空格，然后在运算符和括号的前后加上空格来作为分隔符
def format_formula(formula):
    not_space_formula = formula.replace(' ', '')
    formula_list = []
    formula_in_text = ''
    for value in not_space_formula:
        if value in ['+', '-', '*', '/', '(', ')']:
            formula_list.append(' ' + value + ' ')
        elif value.isnumeric() or value == '.':
            formula_list.append(value)
        else:
            print(value)
            raise ValueError
    for value in formula_list:
        formula_in_text = formula_in_text + value
    return formula_in_text.split()


# 输入算式，返回解析树（二叉树）
def build_parse_tree(formula):
    formula_list = format_formula(formula)
    node_stack = Stack()  # 将所有节点都压进栈来获取父节点
    formula_tree = BinaryTree('')
    node_stack.push(formula_tree)
    # 当前节点
    current_tree = formula_tree
    # 根据算式内容生成节点
    # 由于使用二叉树来，所以只能对两个对象进行运算，例如可以：(3+(4+5)) ,而不能(3+4+5)
    for i in formula_list:
        if i == '(':
            current_tree.insert_left('')
            node_stack.push(current_tree)
            current_tree = current_tree.get_left_child()
        # 判断是否数字字符串，或者包含小数点（浮点数）
        elif i.isnumeric() or i.find('.') > 0:
            current_tree.set_root_value(float(i))
            parent = node_stack.pop()
            current_tree = parent
        elif i in ['+', '-', '*', '/']:
            current_tree.set_root_value(i)
            current_tree.insert_right('')
            node_stack.push(current_tree)
            current_tree = current_tree.get_right_child()
        elif i == ')':
            current_tree = node_stack.pop()
        else:
            print(i)
            raise ValueError
    return formula_tree


# 判断当前节点是否有左右节点，有则进行计算，没有的话就返回当前节点值
def evaluate(parse_tree):
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    left_node = parse_tree.get_left_child()
    right_node = parse_tree.get_right_child()
    if left_node and right_node:
        op = operators[parse_tree.get_root_value()]
        return op(evaluate(left_node), evaluate(right_node))  # 递归
    else:
        return parse_tree.get_root_value()


# 作用同evaluate,但用后序遍历
def postorder_evaluate(tree):
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    left_node = None
    right_node = None
    if tree:
        left_node = postorder_evaluate(tree.get_left_child())
        right_node = postorder_evaluate(tree.get_right_child())
        if left_node and right_node:
            return operators[tree.get_root_value()](left_node, right_node)
        else:
            return tree.get_root_value()

if __name__ == '__main__':
    t1 = build_parse_tree('((10*10)*(30+(34-(10.2+3.8))))')
    print(evaluate(t1))
    print(postorder_evaluate(t1))
