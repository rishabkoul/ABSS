# Generated by Django 3.1.7 on 2021-03-25 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('subdistrict', models.CharField(max_length=100)),
                ('officename', models.CharField(max_length=100)),
                ('villagename', models.CharField(max_length=100)),
                ('pincode', models.BigIntegerField()),
            ],
        ),
    ]
