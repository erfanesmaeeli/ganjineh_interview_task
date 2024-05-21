from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from main.models import TimeGeneral
from django.db.models import Q
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from main.models import TimeGeneral
from . utils import USER_DEFAULT_CREDITS


class Subscription(TimeGeneral):
    LEVEL_CHOICES = [
        (1, 'Gold'),
        (2, 'Silver'),
    ]
    title = models.CharField(max_length=128, null=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, null=True)
    days_to_expire = models.PositiveIntegerField(null=True, )
    # access_tokens = 

    class Meta:
        ordering = ('level',)

    def __str__(self) -> str:
        return self.title + ' - ' + self.get_level
    
    @property
    def get_level(self):
        return dict(self.LEVEL_CHOICES)[self.level]


class User(AbstractUser):
    credits = models.PositiveBigIntegerField(default=USER_DEFAULT_CREDITS)
    
    class Meta:
        verbose_name_plural = _('users')
        verbose_name = _('user')

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username
    
    def get_user_subscription(self):
        if self.subscriptions:
            subscriptions = self.subscriptions.filter(is_active=True, status='approved')
            if subscriptions.exists():
                subscription = subscriptions.first()
                return subscription
        return None
    

class RegisteredSubscription(TimeGeneral):
    STATUS_CHOICES = [
        ('requested', 'requested'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ]

    CREDITS_PERIOD = [
        ('daily', 'daily'),
        ('unlimited', 'unlimited')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='subscriptions')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, related_name='registered_subscriptions')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True, default='requested')
    expire_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    credits = models.PositiveBigIntegerField(null=True, default=USER_DEFAULT_CREDITS)
    credits_period = models.CharField(max_length=10, choices=CREDITS_PERIOD, default='daily')    
    credits_added = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self) -> str:
        return f"{self.user} - {self.subscription} "