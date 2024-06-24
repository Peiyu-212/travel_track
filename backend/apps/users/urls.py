from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .api.viewsets import UsersViewSet

router = DefaultRouter()

router.register('', UsersViewSet, basename='Users')

urlpatterns = [
    path('', include(router.urls)),
]
