# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perap', '0011_auto_20170405_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='characteristic',
            name='value',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='observation',
            name='specified_characteristics',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
