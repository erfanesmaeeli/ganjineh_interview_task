from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from main.utils import custom_date_parser
from .models import *
from datetime import datetime, timedelta
import pandas as pd


@receiver(post_save, sender=CoinPriceFile)
def update_coin_prices(sender, instance , created, **kwargs):
    file = instance.file
    dbframe = pd.read_csv(file, parse_dates=['Date'], date_parser=custom_date_parser)
    coin = instance.coin

    for column in dbframe.itertuples():
        object, created = CoinPrice.objects.get_or_create(date=column.Date, price=column.Price, coin=coin)
        
        # Update Price
        if not created:
            object.price = column.Price
            object.save()
