# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-20 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifs', '0004_auto_20180120_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inorder',
            name='place_in_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
