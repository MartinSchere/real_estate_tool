# Generated by Django 3.1 on 2020-09-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200927_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='setting',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
