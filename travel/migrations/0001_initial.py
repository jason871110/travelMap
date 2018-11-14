# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IMG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('img', models.ImageField(upload_to='upload')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100, blank=True)),
                ('days', models.IntegerField(blank=True)),
                ('schedule_content', models.TextField(blank=True)),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TotalCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day', models.IntegerField(blank=True)),
                ('site_content', models.TextField(blank=True)),
                ('course', models.ForeignKey(to='travel.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='TouristSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('route_order', models.IntegerField()),
                ('site_name', models.CharField(max_length=100)),
                ('time', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='upload')),
                ('line', models.ForeignKey(to='travel.TotalCourse')),
            ],
        ),
    ]
