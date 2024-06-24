from django.db import models


# Create your models here.
class Countries(models.Model):
    country_code = models.CharField(max_length=3, unique=True, null=False)
    country_name = models.CharField(max_length=200, null=False)


class VisitedCountries(models.Model):
    country_code = models.CharField(max_length=2, null=False)
    user = models.ForeignKey('users.Users', related_name='visited_countries_user',
                             on_delete=models.CASCADE)


class TravelExpense(models.Model):
    description = models.CharField(max_length=100, null=False)
    cost = models.IntegerField()
    user_country = models.ForeignKey('VisitedCountries', related_name='user_visit_country',
                                     on_delete=models.CASCADE)
    sightseeing = models.CharField(max_length=100, null=False)
    visited_date = models.DateField(null=False)
