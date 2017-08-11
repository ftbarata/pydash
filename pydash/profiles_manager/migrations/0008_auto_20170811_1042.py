# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_manager', '0007_auto_20170809_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Perfil', 'verbose_name_plural': 'Perfis'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='notification_groups',
            field=models.ManyToManyField(blank=True, to='core.Group', verbose_name='Grupos de notificação de e-mail'),
        ),
    ]