# Generated by Django 3.0.3 on 2020-07-20 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200721_0453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_total',
            new_name='total',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default=0, max_length=120),
            preserve_default=False,
        ),
    ]