# Generated by Django 4.2.13 on 2024-05-22 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_subscription_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='credits',
            field=models.BigIntegerField(default=10),
        ),
    ]
