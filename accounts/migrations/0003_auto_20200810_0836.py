# Generated by Django 3.0.3 on 2020-08-10 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join Time'),
        ),
    ]