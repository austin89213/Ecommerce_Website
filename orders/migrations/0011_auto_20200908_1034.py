# Generated by Django 3.0.3 on 2020-09-08 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_productpurchased_productpurchasedmanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchased',
            name='user',
        ),
        migrations.AddField(
            model_name='productpurchased',
            name='order_id',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
