# Generated by Django 2.1.2 on 2018-12-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_auto_20181128_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristsite',
            name='image',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
