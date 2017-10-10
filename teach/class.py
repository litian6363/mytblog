#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')
        
class duck(object):
    def run(self):
        print('duck')

def run_twice(animal):
    animal.run()
    animal.run()

a = Animal()
d = Dog()
c = Cat()
dd = duck()

print('a is Animal?', isinstance(a, Animal))
print('a is Dog?', isinstance(a, Dog))
print('a is Cat?', isinstance(a, Cat))

print('d is Animal?', isinstance(d, Animal))
print('d is Dog?', isinstance(d, Dog))
print('d is Cat?', isinstance(d, Cat))

print('dd is Animal?', isinstance(dd, Animal))
print('dd is Dog?', isinstance(dd, Dog))
print('dd is Cat?', isinstance(dd, Cat))
print('dd is duck?', isinstance(dd, duck))

run_twice(d)
run_twice(dd)