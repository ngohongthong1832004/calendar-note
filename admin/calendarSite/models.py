from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=9999)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=8)
    alert = models.BooleanField(default=False)
