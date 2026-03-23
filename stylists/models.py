from django.db import models
from accounts.models import User

class Stylist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    specialty = models.CharField(max_length=255, blank=True)
    working_days = models.JSONField(default=list, blank=True)