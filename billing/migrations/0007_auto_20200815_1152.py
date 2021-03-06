# Generated by Django 3.0.3 on 2020-08-15 03:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_charge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='default_payment',
            new_name='default',
        ),
        migrations.AddField(
            model_name='card',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='card',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
