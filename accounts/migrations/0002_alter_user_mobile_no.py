# Generated by Django 5.0.2 on 2024-03-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_no',
            field=models.CharField(blank=True, null=True, unique=True, verbose_name='MobNumber'),
        ),
    ]
