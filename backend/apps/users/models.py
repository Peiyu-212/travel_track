from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(null=False, max_length=20)
    color = models.CharField(null=False, max_length=20)
