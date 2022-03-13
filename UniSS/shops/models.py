from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=2500)
    unique_name = models.CharField(max_length=100)
    description = models.TextField()
    managers = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    