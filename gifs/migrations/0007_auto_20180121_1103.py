# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-21 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifs', '0006_inorder_to_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inorder',
            name='to_public',
            field=models.NullBooleanField(default=None),
        ),
    ]
