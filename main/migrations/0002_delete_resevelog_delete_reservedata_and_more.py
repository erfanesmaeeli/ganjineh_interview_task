# Generated by Django 4.1.7 on 2023-03-18 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReseveLog',
        ),
        migrations.DeleteModel(
            name='ReserveData',
        ),
        migrations.DeleteModel(
            name='WpHotelBookingOrderItemmeta',
        ),
        migrations.DeleteModel(
            name='WpPostmeta',
        ),
        migrations.DeleteModel(
            name='WpPosts',
        ),
    ]
