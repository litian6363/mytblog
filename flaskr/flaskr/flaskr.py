#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)

# flask-sqlalchemy的数据库配置
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/testsc?charset=utf8'

# flask config，全局？
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
# flask默认配置
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# 模板
class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.String(500), unique=True, nullable=False)
    create_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Entries %r>' % self.title


@app.route('/')
def show_entries():
    i = 0
    cur = []
    # SQLAlchemy可以query(title, text), flask-sqlalchemy不可以,只能query,不能有括号在后面
    results = Entries.query.order_by(Entries.id).all()
    return render_template('show_entries.html', entries=results)


@app.route('/add', methods=['POST'])
def add_entry():
    # 如果没有登录就报错
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    text = request.form['text']
    new_entries = Entries(title=title, text=text)
    db.session.add(new_entries)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        # 丑陋的验证
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# set FLASK_APP= flask
# set FLASK_DEBUG=true
# flask  run

if __name__ == '__main__':
    # 删除全部表，创建全部表
    # db.drop_all()
    # db.create_all()
    app.run()




