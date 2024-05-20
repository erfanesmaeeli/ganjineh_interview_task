from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from main.models import General
from django.db.models import Q
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime
from django.utils.translation import gettext as _


class User(AbstractUser):

    class Meta:
        verbose_name_plural = _('users')
        verbose_name = _('user')

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username