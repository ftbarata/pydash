# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170714_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='detailed_message',
            field=models.TextField(default=django.utils.timezone.now, max_length=1000, verbose_name='Mensagem técnica'),
            preserve_default=False,
        ),
    ]
