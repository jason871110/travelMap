# Generated by Django 2.1.3 on 2018-12-01 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_auto_20181128_0057'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Schedule_content',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='created_at',
        ),
        migrations.AddField(
            model_name='touristsite',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
