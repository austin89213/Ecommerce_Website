# Generated by Django 3.0.3 on 2020-09-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20200728_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
