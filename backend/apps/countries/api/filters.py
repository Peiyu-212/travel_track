from django_filters import rest_framework as filters

from ..models import TravelExpense


class TravelExpenseFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user_country__user__name', lookup_expr='iexact')
    country_code = filters.CharFilter(field_name='user_country__country_code', lookup_expr='iexact')
    sightseeing = filters.CharFilter(field_name='sightseeing', lookup_expr='icontains')

    class Meta:
        model = TravelExpense
        fields = '__all__'
