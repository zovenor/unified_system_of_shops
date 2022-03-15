from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class ApplicationToken(models.Model):
    name = models.CharField(max_length=250, unique=True)
    key = models.CharField(max_length=32, default=get_random_string(32), unique=True, editable=False)

    def __str__(self):
        return f'{self.name}  -  {self.key}'

    def change(self):
        self.key = get_random_string(32)


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

    def shop_around(self, your_location):
        your_lat = your_location[0]
        your_lng = your_location[1]
        __degree__ = 111.134861111

        lat = self.lat
        lng = self.lng

        distance = ((your_lng - lng) ** 2 + (your_lat - lat) ** 2) ** (1.0 / 2) * __degree__

        if distance < 0.5:
            return True


class Product(models.Model):
    name = models.CharField(max_length=2500)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
