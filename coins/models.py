from django.db import models
from main.models import TimeGeneral


class Coin(TimeGeneral):
    name = models.CharField(max_length=64, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.name
    

class CoinPrice(TimeGeneral):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True, related_name='prices')
    price = models.FloatField(null=True)
    date = models.DateField()

    class Meta:
        ordering = ('-date', 'coin')

    def __str__(self) -> str:
        return self.coin.name + ' - ' + str(self.price) + ' - ' + self.get_date
    
    @property
    def get_date(self):
        return self.date.strftime("%m/%d/%y")
    

class CoinPriceFile(TimeGeneral):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='coins/prices/')
