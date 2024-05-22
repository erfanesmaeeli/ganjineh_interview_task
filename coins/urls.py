from django.urls import path
from .views import *

app_name = 'coins'

urlpatterns = [
    path('coins/', CoinView.as_view(), name='coins'),
]