from django.urls import include, path

# RESTful api router
from rest_framework.routers import DefaultRouter

from .api.viewsets import CountryViewSet, TravelExpenseViewSet, VisitedCountriesViewSet

router = DefaultRouter()
router.register('country', CountryViewSet, basename='country_default')
router.register('visit_country', VisitedCountriesViewSet, basename='visit_country')
router.register('travel_expense', TravelExpenseViewSet, basename='travel_expense')

urlpatterns = [
    path('', include(router.urls))
]
