# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_observedcharacteristic_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='observedcharacteristic',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.Item'),
            preserve_default=False,
        ),
    ]
