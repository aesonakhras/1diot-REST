# Generated by Django 2.2.9 on 2020-01-03 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20200102_0532'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rooms',
            new_name='Room',
        ),
    ]
