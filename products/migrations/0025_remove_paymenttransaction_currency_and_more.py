# Generated by Django 5.0.2 on 2024-03-29 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_remove_sizechart_quantity_product_sku_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='muid',
        ),
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='subtotal_qty',
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='address',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='items',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='payment_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('online', 'Online'), ('bank_transfer', 'Bank Transfer'), ('cod', 'COD')], max_length=20),
        ),
    ]
