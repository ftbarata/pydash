# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Foto de perfil'),
        ),
    ]
