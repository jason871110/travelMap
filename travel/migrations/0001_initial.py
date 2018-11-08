# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100, blank=True)),
                ('content', models.TextField(blank=True)),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TouristSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('site_name', models.CharField(max_length=100)),
                ('route_order', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='upload')),
                ('course', models.ForeignKey(to='travel.Course')),
            ],
        ),
    ]
