# Generated by Django 5.0.2 on 2024-02-19 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_data', '0004_rename_refundcancellationpolicyterms_refundcancellationpolicy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='termsandcondition',
            old_name='title',
            new_name='section',
        ),
    ]
