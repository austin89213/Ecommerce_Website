# Generated by Django 3.0.3 on 2020-08-14 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default_payment',
            field=models.BooleanField(default=True),
        ),
    ]
