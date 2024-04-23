# Generated by Django 5.0.2 on 2024-04-23 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gst_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='GstNumber'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pan_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='PanNumber'),
        ),
    ]
