# Generated by Django 3.0.3 on 2020-07-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200721_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
