from django.db import models
from django.contrib.auth.models import User


class ShopChain(models.Model):
    name = models.CharField(max_length=2500)
    unique_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    managers = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Shop(models.Model):
    chain = models.ForeignKey(ShopChain, on_delete=models.CASCADE)
    managers = models.ManyToManyField(User)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f'{self.chain.name} shop{self.id}'


class Product(models.Model):
    name = models.CharField(max_length=2500)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
