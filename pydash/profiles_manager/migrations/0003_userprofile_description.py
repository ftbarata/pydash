# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_manager', '0002_auto_20170724_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição'),
        ),
    ]
