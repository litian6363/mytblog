#!usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemylearn.mysqlengine import Session, User

session = Session()
ed_user = User(name='ed', fullname='Ed Jones', password='edpassword')
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first()
print('end')
print(our_user)
if ed_user is our_user: print('True')
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
ed_user.password = 'f8s7ccs'
print(session.dirty)
print(session.new)
session.commit()
print(ed_user.id)
