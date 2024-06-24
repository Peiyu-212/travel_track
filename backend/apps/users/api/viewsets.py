from rest_framework import viewsets

from ..models import Users
from .serializer import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
