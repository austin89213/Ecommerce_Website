# Generated by Django 3.0.3 on 2020-09-06 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_digital',
            field=models.BooleanField(default=False),
        ),
    ]
