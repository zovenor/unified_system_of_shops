from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField


class ChainShop(models.Model):
    name = models.CharField(max_length=2500)
    unique_name = models.CharField(max_length=100)
    description = models.TextField()
    managers = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Shop(models.Model):
    chain = models.ForeignKey(ChainShop, on_delete=models.CASCADE)
    managers = models.ManyToManyField(User)
    location = PlainLocationField()

    def __str__(self):
        return self.chain.name


class Product(models.Model):
    name = models.CharField(max_length=2500)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
