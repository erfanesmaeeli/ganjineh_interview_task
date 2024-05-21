from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import *
from datetime import datetime, timedelta
import pandas as pd


@receiver(post_save, sender=CoinPriceFile)
def update_coin_prices(sender, instance , created, **kwargs):
    file = instance.file
    dbframe = pd.read_csv(file)
    data_list = []
    coin = instance.coin
    for column in dbframe.itertuples():
        date = column.Date.replace('/', '-').split('-')
        date = datetime(year=int(date[2]), month=int(date[0]), day=int(date[1]))
        object, created = CoinPrice.objects.get_or_create(date=date, price=column.Price, coin=coin)
        
        # Update Price
        if not created:
            object.price = column.Price
            object.save()
