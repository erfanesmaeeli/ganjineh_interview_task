from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import CoinPrice, Coin
from .serializers import CoinPriceSerializer, PeriodSerializer
from .filters import CoinPriceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import *
from datetime import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.utils import USER_DEFAULT_ACCESS_COINS
from accounts.permissions import PremiumUserPermission
from . utils import MAX_PROFIT_AND_LOSS_PERIODS


class CoinPriceListView(generics.ListAPIView):
    queryset = CoinPrice.objects.all()
    serializer_class = CoinPriceSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoinPriceFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('coin_name', openapi.IN_QUERY, description="Coin Name", type=openapi.TYPE_STRING),
        openapi.Parameter('date_from', openapi.IN_QUERY, description="Date From (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter('date_to', openapi.IN_QUERY, description="Date To (YYYY-MM-DD)", type=openapi.TYPE_STRING),
    ])

    def list(self, request, *args, **kwargs):
        user = self.request.user

        # Check if the coin, date_form and date_to filter is provided
        coin_name = self.request.query_params.get('coin_name')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if not coin_name:
            return Response({"error": "You must provide a coin_name to filter by."}, status=HTTP_200_OK)

        if not date_from:
            return Response({"error": "You must provide a date_from to filter by."}, status=HTTP_200_OK)

        if not date_to:
            return Response({"error": "You must provide a date_to to filter by."}, status=HTTP_200_OK)

        try:
            coin = Coin.objects.get(name=coin_name)
        except Exception as e:
            return Response(
                {"error": "Invalid coin name"},
                status=HTTP_400_BAD_REQUEST)
        
        # Normal User Limitions
        if not user.get_user_subscription():
            # Check the date range for normal users
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                date_diff = (date_to_obj - date_from_obj).days
                if date_diff > 30:
                    return Response(
                        {"error": "The date range must not be greater than 30 days. Please subscribe to premium."},
                        status=HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=HTTP_400_BAD_REQUEST
            )

            # Check the coin filtered for normal users
            if coin.name not in USER_DEFAULT_ACCESS_COINS:
                return Response(
                    {"error": "Limited access. Buy a special subscription to see more coins!"},
                    status=HTTP_403_FORBIDDEN
            )

        # Decrement user credits
        if user.credits <= 0:
            return Response({"error": "Insufficient credits"}, status=HTTP_403_FORBIDDEN)
        
        user.decrement_credits(coin.credits)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ProfitablePeriodsView(generics.ListAPIView):
    serializer_class = PeriodSerializer
    permission_classes = [PremiumUserPermission]
    filter_backends = [DjangoFilterBackend]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('coin_name', openapi.IN_QUERY, description="Coin name", type=openapi.TYPE_STRING),
            openapi.Parameter('date_from', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('date_to', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: PeriodSerializer(many=True)}
    )

    def get_queryset(self):
        return CoinPrice.objects.none()

    def list(self, request, *args, **kwargs):
        user = self.request.user

        coin_name = request.query_params.get('coin_name')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if not coin_name:
            return Response({"error": "You must provide a coin_name to filter by."}, status=HTTP_200_OK)

        if not date_from:
            return Response({"error": "You must provide a date_from to filter by."}, status=HTTP_200_OK)

        if not date_to:
            return Response({"error": "You must provide a date_to to filter by."}, status=HTTP_200_OK)

        try:
            coin = Coin.objects.get(name=coin_name)
        except Exception as e:
            return Response(
                {"error": "Invalid coin name"},
                status=HTTP_400_BAD_REQUEST)
        
        # Decrement user credits
        if user.credits < 10:
            return Response({"error": "Insufficient credits"}, status=HTTP_403_FORBIDDEN)
        
        user.decrement_credits(10)


        coin_prices = CoinPrice.objects.filter(coin=coin, date__range=[date_from, date_to]).order_by('date')
        if not coin_prices.exists():
            return Response({"error": "No price data available for the given range."}, status=HTTP_400_BAD_REQUEST)

        profitable_periods = self.get_profitable_periods(coin_prices)

        serializer = self.get_serializer(profitable_periods, many=True)
        return Response(serializer.data)

    def get_profitable_periods(self, coin_prices):
        periods = []
        max_periods = MAX_PROFIT_AND_LOSS_PERIODS

        for i in range(len(coin_prices) - 1):
            for j in range(i + 1, len(coin_prices)):
                period_profit = coin_prices[j].price - coin_prices[i].price
                periods.append((period_profit, coin_prices[i], coin_prices[j]))

        periods.sort(reverse=True, key=lambda x: x[0])
        top_periods = periods[:max_periods]

        return [{'start': period[1], 'end': period[2], 'profit': period[0]} for period in top_periods]


class LossMakingPeriodsView(ProfitablePeriodsView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('coin_name', openapi.IN_QUERY, description="Coin name", type=openapi.TYPE_STRING),
            openapi.Parameter('date_from', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('date_to', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: PeriodSerializer(many=True)}
    )
    
    def get_profitable_periods(self, coin_prices):
        periods = []
        max_periods = MAX_PROFIT_AND_LOSS_PERIODS

        for i in range(len(coin_prices) - 1):
            for j in range(i + 1, len(coin_prices)):
                period_loss = coin_prices[i].price - coin_prices[j].price
                periods.append((period_loss, coin_prices[i], coin_prices[j]))

        periods.sort(reverse=True, key=lambda x: x[0])
        top_periods = periods[:max_periods]

        return [{'start': period[1], 'end': period[2], 'loss': period[0]} for period in top_periods]