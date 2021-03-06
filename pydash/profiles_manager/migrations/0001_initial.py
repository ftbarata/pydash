# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Foto de perfil')),
                ('username', models.CharField(max_length=30, verbose_name='Usuário')),
                ('email', models.EmailField(max_length=50)),
                ('lotacao', models.CharField(max_length=20, verbose_name='Lotação')),
                ('phone', models.CharField(max_length=15, verbose_name='Telefone')),
            ],
        ),
    ]
