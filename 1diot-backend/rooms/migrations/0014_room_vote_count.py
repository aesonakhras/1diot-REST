# Generated by Django 2.2.9 on 2020-01-08 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0013_auto_20200107_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
