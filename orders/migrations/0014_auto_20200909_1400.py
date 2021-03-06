# Generated by Django 3.0.3 on 2020-09-09 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_is_digital'),
        ('orders', '0013_delete_productpurchasemanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpurchase',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='purchased', to='products.Product'
            ),
        ),
    ]
