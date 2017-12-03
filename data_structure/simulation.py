#!usr/bin/env python3
# -*- coding: utf-8 -*-


# 模拟栈
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)

# # 栈测试
# if __name__ == '__main__':
#     s = Stack()
#     print(s.is_empty())
#     s.push(4)
#     s.push('dog')
#     print(s.peek())
#     s.push(True)
#     print(s.size())
#     print(s.is_empty())
#     s.push(8.4)
#     print(s.pop())
#     print(s.pop())
#     print(s.size())
#     print(s.stack)
#     print('栈测试完成\n')


# 模拟队列
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.insert(0, item)

    def dequeue(self):
        return self.queue.pop()

    def is_empty(self):
        return self.queue == []

    def size(self):
        return len(self.queue)


# # 队列测试
# if __name__ == '__main__':
#     q = Queue()
#     print(q.is_empty())
#     q.enqueue(4)
#     q.enqueue('dog')
#     q.enqueue(True)
#     print(q.size())
#     print(q.dequeue())
#     print(q.dequeue())
#     print(q.dequeue())
#     print(q.is_empty())
#     print('队列测试完成\n')


# # 用嵌套列表来实现二叉树

# if __name__ == '__main__':
#     myTree = ['a', ['b', ['d', [], []], ['e', [], []]], ['c', ['f', [], []], []]]
#     print(myTree)
#     print('left subtree = ', myTree[1])
#     print('root = ', myTree[0])
#     print('right subtree = ', myTree[2])
#     print('r1 = ', myTree[2][1])
#     print('END------')


def binary_tree(r):
    return [r, [], []]


def insertLeft(root, newBranch):
    t = root.pop(1)
    if len(t) > 1:
        root.insert(1, [newBranch, t, []])
    else:
        root.insert(1, [newBranch, [], []])
    return root


def insertRight(root, newBranch):
    t = root.pop(2)
    if len(t) > 1:
        root.insert(2, [newBranch, [], t])
    else:
        root.insert(2, [newBranch, [], []])
    return root


def getRootVal(root):
    return root[0]


def setRootVal(root, newVal):
    root[0] = newVal


def getLeftChild(root):
    return root[1]


def getRightChild(root):
    return root[2]

# if __name__ == '__main__':
#     r = binary_tree(3)
#     insertLeft(r, 4)
#     insertLeft(r, 5)
#     insertRight(r, 6)
#     insertRight(r, 7)
#     l = getLeftChild(r)
#     print(l)
#
#     setRootVal(l, 9)
#     print(r)
#     insertLeft(l, 11)
#     print(r)
#     print(getRightChild(getRightChild(r)))
#     print('嵌套树测试结束\n')


# 节点类和应用
class BinaryTree:
    def __init__(self, root_object):
        self.key = root_object
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if not self.left_child:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if not self.right_child:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_value(self, root_object):
        self.key = root_object

    def get_root_value(self):
        return self.key

# if __name__ == '__main__':
#     r = BinaryTree('a')
#     print(r.get_root_value())
#     print(r.get_left_child())
#     r.insert_left('b')
#     print(r.get_left_child())
#     print(r.get_left_child().get_root_value())
#     r.insert_right('c')
#     print(r.get_right_child())
#     print(r.get_right_child().get_root_value())
#     r.get_right_child().set_root_value('hello')
#     print(r.get_right_child().get_root_value())
#     r.get_right_child().insert_right('d')
#     print(r.get_right_child().get_right_child().get_root_value())
#     print('类二叉树测试结束\n')
