# Generated by Django 4.2.13 on 2024-05-21 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinprice',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
