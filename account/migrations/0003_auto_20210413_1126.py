# Generated by Django 3.1.7 on 2021-04-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210413_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=60, verbose_name='email'),
        ),
    ]
