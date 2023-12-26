from django.db import models

class Details(models.Model):
    name = models.CharField(max_length = 40)
    profile = models.CharField(max_length=60)