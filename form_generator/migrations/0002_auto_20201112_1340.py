# Generated by Django 3.1 on 2020-11-12 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_generator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='field',
            old_name='name',
            new_name='question',
        ),
    ]
