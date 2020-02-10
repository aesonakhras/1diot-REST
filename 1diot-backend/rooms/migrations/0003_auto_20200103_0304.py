# Generated by Django 2.2.9 on 2020-01-03 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20200103_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='username')),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='user_list',
            field=models.TextField(blank=True),
        ),
    ]