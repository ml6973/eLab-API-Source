# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20161116_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
