from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import RegisteredSubscription, User
from datetime import datetime, timedelta 


@receiver(post_save, sender=User)
def update_registered_subscription_activation(sender,instance , **kwargs):
    user_subscription = instance.get_user_subscription()
    if user_subscription and user_subscription.credits_period == 'unlimited':
        if instance.credits < 1:
            user_subscription.is_active = False
            user_subscription.save()