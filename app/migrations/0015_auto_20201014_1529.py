# Generated by Django 3.1 on 2020-10-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20201014_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='zpid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
