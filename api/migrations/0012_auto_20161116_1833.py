# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 00:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20161116_1826'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='instance',
            unique_together=set([('cloud', 'computeId')]),
        ),
    ]
