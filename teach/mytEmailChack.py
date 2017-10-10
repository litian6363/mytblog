#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def emailChack(st):
    if st[0]==r'<':
        if re.match(r'^\<(\w*)\>(\w[\w\.]*@\w\w*)\.(com|org)$',st):
            st = re.match(r'^\<(\w*)\>(\w[\w\.]*@\w\w*)\.(com|org)$',st).groups()
            return(st)
        else : raise ValueError('Name wrong format!')
    elif re.match(r'^(\w[\w\.]*)@(\w\w*)\.(com$)',st):
        return(st)
    else :
        raise ValueError('Wrong format!')
        
        
if __name__ == '__main__' :

    value = input('请输入邮箱:')
    print(emailChack(value))