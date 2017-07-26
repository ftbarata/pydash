# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170710_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Grupos'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.CharField(default='Sistema', max_length=100, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Mensagem'),
        ),
        migrations.AlterField(
            model_name='message',
            name='severity',
            field=models.CharField(max_length=20, verbose_name='Severidade'),
        ),
    ]
