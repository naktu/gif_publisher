# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifs', '0010_auto_20180208_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gif',
            name='file',
        ),
    ]
