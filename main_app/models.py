from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Photo(models.Model):
    name = models.CharField(max_length=300)
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)