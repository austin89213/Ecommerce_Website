# Generated by Django 3.0.3 on 2020-08-15 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_card_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
