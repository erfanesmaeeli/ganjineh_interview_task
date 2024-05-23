from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from main.models import TimeGeneral
from django.db.models import Q
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from main.models import TimeGeneral
from main.utils import send_email
from . utils import USER_DEFAULT_CREDITS
from coins.models import Coin
from django.core.mail import EmailMessage
from django.template.loader import get_template
import jdatetime


class Subscription(TimeGeneral):
    LEVEL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]
    title = models.CharField(max_length=128, null=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, null=True)
    days_to_expire = models.PositiveIntegerField(null=True, )


    class Meta:
        ordering = ('level',)

    def __str__(self) -> str:
        return self.title + ' - ' + self.get_level
    
    @property
    def get_level(self):
        return dict(self.LEVEL_CHOICES)[self.level]


class User(AbstractUser):
    credits = models.BigIntegerField(default=USER_DEFAULT_CREDITS)
    
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
    
    def access_all_coins(self):
        user_subscription = self.get_user_subscription()
        if user_subscription:
            return True
        return False
    access_all_coins.boolean = True


    def decrement_credits(self, amount):
        self.credits -= amount
        self.save()
    

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__pre_status = self.status
        self.__pre_is_active = self.is_active

    def save(self, *args, **kwargs):
        jalali_today = jdatetime.datetime.today().strftime('%H:%M - %Y/%m/%d')
        today = datetime.today().date()
        email_template = 'accounts/subscription_email_text.html'
        user = self.user
        if self.__pre_status != self.status:
            if self.status == 'approved':
                self.is_active = True
                if self.subscription.level == 'gold' and not self.credits_added:
                    self.user.credits = self.credits
                    self.credits_added = True
                    self.user.save()

                if not self.expire_at:
                    days_to_expire = self.subscription.days_to_expire
                    expire_at = today + timedelta(days=days_to_expire)
                    self.expire_at = expire_at

                email_subject = 'تایید سفارش'
                body = f"درخواست اشتراک {self.subscription.title} با موفقیت تایید و بر روی حساب کاربری شما فعال گردید."
                data = {
                    'today' :jalali_today,
                    'email_subject' : email_subject,
                    'user' : user,
                    'email_body': body
                }
                send_email(data=data, to_user=user.email, subject=email_subject, \
                           email_template=email_template)
            elif self.status == 'rejected':
                self.is_active = False
                email_subject = 'عدم تایید سفارش'
                body = f"درخواست اشتراک {self.subscription.title} عدم تایید شد. در صورت نیاز با پشتیبان تماس بگیرید."
                data = {
                    'today' :jalali_today,
                    'email_subject' : email_subject,
                    'user' : user,
                    'email_body': body
                }
                send_email(data=data, to_user=user.email, subject=email_subject, \
                           email_template=email_template)
        if self.__pre_is_active != self.is_active:
            if not self.is_active:
                if today > self.expire_at:
                    email_subject = 'منقضی شدن زمان اشتراک'
                    body = f"مهلت زمانی اشتراک {self.subscription.title} به اتمام رسیده است. جهت ثبت سفارش جدید از طریق وب سایت مراجعه فرمایید."
                    data = {
                        'today' :today,
                        'email_subject' : email_subject,
                        'user' : user,
                        'email_body': body
                    }
                elif self.credits_period == 'unlimited':
                    email_subject = 'اتمام کردیت اشتراک'
                    body = "تعداد کردیت‌های اشتراک {self.subscription.title} به اتمام رسیده است. جهت ثبت سفارش جدید از طریق وب سایت مراجعه فرمایید."
                    data = {
                        'today' :today,
                        'email_subject' : email_subject,
                        'user' : user,
                        'email_body': body
                    }
        super().save(*args, **kwargs)