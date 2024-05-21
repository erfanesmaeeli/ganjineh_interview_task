from django.db import models
from jalali_date import datetime2jalali, date2jalali
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext as _


# ----------------------- General Models  -----------------------
class TimeGeneral(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_jalali_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')

    def get_jalali_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')
# ----------------------- end General Models  -----------------------