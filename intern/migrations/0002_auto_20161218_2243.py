# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-18 21:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    atomic=False

    dependencies = [
        ('intern', '0001_initial'),
    ]

    database_operations = [
        migrations.AlterModelTable('interngroup', 'core_group')
    ]

    state_operations = [

    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations
        )
    ]
