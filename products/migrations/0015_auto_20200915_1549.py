# Generated by Django 3.0.3 on 2020-09-15 07:49

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_productfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(
                storage=django.core.files.storage.FileSystemStorage(
                    location='C:\\Users\\kira8\\Desktop\\Coding\\Django\\Django_Stuff\\Ecommerce_Website\\protected_media'
                ),
                upload_to=products.models.upload_product_file_location
            ),
        ),
    ]
