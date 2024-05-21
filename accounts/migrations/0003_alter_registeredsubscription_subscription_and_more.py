# Generated by Django 4.2.13 on 2024-05-21 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_subscription_user_credits_registeredsubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredsubscription',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registered_subscriptions', to='accounts.subscription'),
        ),
        migrations.AlterField(
            model_name='registeredsubscription',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]