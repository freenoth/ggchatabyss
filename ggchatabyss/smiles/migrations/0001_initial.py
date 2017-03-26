# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Smile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gg_id', models.CharField(max_length=10)),
                ('bind', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('donat', models.IntegerField()),
                ('premium', models.IntegerField()),
                ('paid', models.IntegerField()),
                ('animated', models.BooleanField()),
                ('tag', models.CharField(max_length=100)),
                ('img', models.CharField(max_length=255)),
                ('img_big', models.CharField(max_length=255)),
                ('img_gif', models.CharField(max_length=255)),
                ('channel', models.CharField(blank=True, max_length=255, null=True)),
                ('channel_id', models.CharField(max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
