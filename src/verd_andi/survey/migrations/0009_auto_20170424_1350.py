# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 13:50
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('survey', '0008_itemobserver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observer',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='observation',
            name='obeservation_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]