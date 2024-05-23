import traceback
from celery import shared_task
from django.db.models import *
import re
import sys, os
from datetime import datetime, timedelta
from accounts.models import User, RegisteredSubscription
from accounts.utils import USER_DEFAULT_CREDITS


@shared_task
def check_user_subscriptions():
    today = datetime.today().date()
    for user in User.objects.filter(is_active=True):
        user_subscription = user.get_user_subscription()
        if user_subscription:
            if today > user_subscription.expire_at:
                user_subscription.is_active = False
                user_subscription.save()
                user.credits = USER_DEFAULT_CREDITS

            elif user_subscription.credits_period == 'daily':
                    user.credits = user_subscription.credits
        else:
            user.credits = USER_DEFAULT_CREDITS

        user.save()
            