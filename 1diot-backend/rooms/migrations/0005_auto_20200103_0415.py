# Generated by Django 2.2.9 on 2020-01-03 04:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200103_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='user_list',
        ),
        migrations.AddField(
            model_name='room',
            name='user_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), default=[], size=10),
        ),
    ]
