import django_filters
from .models import CoinPrice
from django import forms
from . models import Coin

class CoinPriceFilter(django_filters.FilterSet):
    coin_name = django_filters.CharFilter(
        field_name='coin__name',
        lookup_expr='icontains',
        label='Coin Name',
        help_text='Enter the coin name to filter by.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Coin Name'
        })
    )

    date_from = django_filters.DateFilter(
        field_name="date", 
        lookup_expr='gte', 
        label="Date From",
        help_text="Enter the start date for the filter range.",
        widget=forms.DateInput(attrs={
            'placeholder': 'MM/DD/YYYY',
            'type': 'date'
        })
    )
    date_to = django_filters.DateFilter(
        field_name="date", 
        lookup_expr='lte', 
        label="Date To",
        help_text="Enter the start date for the filter range.",
        widget=forms.DateInput(attrs={
            'placeholder': 'MM/DD/YYYY',
            'type': 'date'
        })
    )

    class Meta:
        model = CoinPrice
        fields = ['coin_name', 'date_from', 'date_to']