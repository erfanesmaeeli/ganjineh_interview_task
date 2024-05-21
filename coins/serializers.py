from rest_framework import serializers
from .models import Coin, CoinPrice


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('id', 'name')


class CoinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPrice
        fields = ('id', 'coin', 'date', 'price')