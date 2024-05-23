from rest_framework import serializers
from .models import Coin, CoinPrice


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class CoinPriceSerializer(serializers.ModelSerializer):
    coin_name = serializers.CharField(source='coin.name', read_only=True)

    class Meta:
        model = CoinPrice
        fields = ('coin_name', 'date', 'price')


class PeriodSerializer(serializers.Serializer):
    start = CoinPriceSerializer()
    end = CoinPriceSerializer()
    profit = serializers.FloatField(required=False)
    loss = serializers.FloatField(required=False)