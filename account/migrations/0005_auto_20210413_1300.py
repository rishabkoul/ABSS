# Generated by Django 3.1.7 on 2021-04-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210413_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(default='notgiven', max_length=60, verbose_name='email'),
        ),
    ]
