# Generated by Django 3.0.3 on 2020-07-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200721_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipeed', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=120),
        ),
    ]
