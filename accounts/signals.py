from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import RegisteredSubscription, User
from datetime import datetime, timedelta


@receiver(pre_save, sender=RegisteredSubscription)
def update_registered_subscription_expire_at(sender, instance , **kwargs):
    if instance.status == 'approved':
        instance.is_active = True
        
        if instance.subscription.level == 1 and not instance.credits_added:
            instance.user.credits = instance.credits
            instance.credits_added = True
            instance.user.save()

        if not instance.expire_at:
            today = datetime.today().date()
            days_to_expire = instance.subscription.days_to_expire
            expire_at = today + timedelta(days=days_to_expire)
            instance.expire_at = expire_at


@receiver(post_save, sender=User)
def update_registered_subscription_activation(sender,instance , **kwargs):
    user_subscription = instance.get_user_subscription()
    if user_subscription and user_subscription.credits_period == 'unlimited':
        if instance.credits < 1:
            user_subscription.is_active = False
            user_subscription.save()