# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_manager', '0003_userprofile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images', verbose_name='Foto de perfil'),
        ),
    ]
