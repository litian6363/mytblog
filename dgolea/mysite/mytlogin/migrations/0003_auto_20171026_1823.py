# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 10:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mytlogin', '0002_users_create_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='user_name',
            new_name='email',
        ),
        migrations.AlterField(
            model_name='users',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 26, 10, 22, 36, 824521, tzinfo=utc), verbose_name='create date'),
        ),
    ]
