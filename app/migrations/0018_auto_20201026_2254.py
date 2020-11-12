# Generated by Django 3.1 on 2020-10-26 22:54

from django.db import migrations, models
import djmoney.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20201023_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='property',
            name='estimated_value',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='USD', help_text='Value generated automatically by zillow, but you can edit freely', max_digits=20, null=True),
        ),
    ]
