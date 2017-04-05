# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 11:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='observation',
            name='observer',
        ),
        migrations.AddField(
            model_name='userobservation',
            name='observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perap.Observation'),
        ),
        migrations.AddField(
            model_name='userobservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]