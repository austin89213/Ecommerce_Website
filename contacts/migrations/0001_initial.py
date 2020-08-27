# Generated by Django 3.0.3 on 2020-08-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('content', models.CharField(max_length=252)),
            ],
        ),
    ]
