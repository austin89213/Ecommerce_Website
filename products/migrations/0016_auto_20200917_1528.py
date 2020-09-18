# Generated by Django 3.0.3 on 2020-09-17 07:28

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200915_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productfile',
            name='user_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\TSAI\\Desktop\\coding\\django\\Django_Stuff\\Ecommerce_Website\\protected_media'), upload_to=products.models.upload_product_file_location),
        ),
    ]
