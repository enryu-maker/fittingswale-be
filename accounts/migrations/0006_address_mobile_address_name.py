# Generated by Django 4.2.14 on 2024-07-21 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_address_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
