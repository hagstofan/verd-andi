# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20170406_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservedCharacteristic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Characteristic')),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Observation')),
            ],
        ),
    ]
