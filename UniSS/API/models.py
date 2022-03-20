from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class ApplicationToken(models.Model):
    name = models.CharField(max_length=250, unique=True)
    key = models.CharField(max_length=32, default=get_random_string(32), unique=True, editable=False)
    active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name}  -  {self.key}'

    def change(self):
        self.key = get_random_string(32)