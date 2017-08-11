# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_notifications', '0002_auto_20170809_1359'),
        ('core', '0014_auto_20170719_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='notification_groups',
            field=models.ManyToManyField(blank=True, to='mail_notifications.NotificationGroup', verbose_name='Grupos de notificação'),
        ),
    ]
