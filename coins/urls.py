from django.urls import path
from .views import *

app_name = 'coins'

urlpatterns = [
    path('prices/', CoinPriceListView.as_view(), name='coins-price-list'),
    path('profitable_periods/', ProfitablePeriodsView.as_view(), name='profitable-periods'),
    path('loss_making_periods/', LossMakingPeriodsView.as_view(), name='loss-making-periods'),
]