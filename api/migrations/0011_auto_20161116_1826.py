# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20161116_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='cloudId',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
