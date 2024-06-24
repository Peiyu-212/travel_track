from rest_framework import serializers

from ..models import Countries, TravelExpense, VisitedCountries


class SingleUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    date = serializers.CharField(required=False)
    user = serializers.CharField(required=False)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = '__all__'


class VisitedCountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitedCountries
        fields = '__all__'


class TravelExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelExpense
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        country = dict(Countries.objects.values_list('country_code', 'country_name'))
        representation['user'] = instance.user_country.user.name
        representation['country_code'] = instance.user_country.country_code
        representation['country_name'] = country.get(representation['country_code'])
        return representation
