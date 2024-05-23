from django.contrib import admin
from . models import *


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits')


@admin.register(CoinPrice)
class CoinPriceAdmin(admin.ModelAdmin):
    list_display = ('coin', 'price', 'get_date')
    list_filter = ('coin', )


@admin.register(CoinPriceFile)
class CoinPriceFileAdmin(admin.ModelAdmin):
    list_display = ('coin',  'created_at')