#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/testsc?charset=utf8'
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.String(500), unique=True, nullable=False)
    create_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Entries %r>' % self.title


# if __name__ == '__main__':
#     db.drop_all()
#     db.create_all()
