# Generated by Django 3.1 on 2020-10-07 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201001_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='zws_id',
        ),
    ]