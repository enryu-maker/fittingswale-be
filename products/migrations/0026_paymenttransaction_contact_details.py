# Generated by Django 5.0.2 on 2024-03-29 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_remove_paymenttransaction_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='contact_details',
            field=models.JSONField(null=True),
        ),
    ]
