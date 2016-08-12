from django.db import models
from django.contrib.auth.models import User

class DrChronoAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100, blank=True)
    refresh_token = models.CharField(max_length=100, blank=True)
    token_expiration = models.DateTimeField(auto_now=True)
