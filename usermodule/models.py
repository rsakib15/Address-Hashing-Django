from django.db import models

# Create your models here.
class User(models.Model):
    address = models.CharField(max_length=255, blank=False)
    hash = models.TextField(blank=False)
    
