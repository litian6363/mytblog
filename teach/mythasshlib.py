#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

db = {}

def calc_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

def login(username,password):
    if calc_md5(password + username + 'ttt') == db[username]: return True
    else : return False
    
def regeister(username,password):
    db[username] = calc_md5(password + username + 'ttt')

    

if __name__ == '__main__':
    
    username = input('请输入用户名：')
    password = input('请输入密码：')
    regeister(username,password)
    if login(username,password) :
        print('yes')


    
    

