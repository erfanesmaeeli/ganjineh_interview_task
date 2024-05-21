from django.contrib import admin
from . models import *


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CoinPrice)
class CoinPriceAdmin(admin.ModelAdmin):
    list_display = ('coin', 'price', 'get_date')
    list_filter = ('coin', )


@admin.register(CoinPriceFile)
class CoinPriceFileAdmin(admin.ModelAdmin):
    list_display = ('coin',  )