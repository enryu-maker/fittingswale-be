# Generated by Django 5.0.2 on 2024-02-25 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_minimum_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maincategory',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='main_category',
        ),
        migrations.AddField(
            model_name='maincategory',
            name='main_category_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='maincategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='main_category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.maincategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category_name',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category')),
                ('category_name', models.CharField(max_length=50, null=True)),
                ('main_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.maincategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
