# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_manager', '0004_auto_20170725_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notification_groups',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Grupos de notificação'),
            preserve_default=False,
        ),
    ]