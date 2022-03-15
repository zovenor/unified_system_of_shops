from django.db import models
from django.utils.crypto import get_random_string


class ApplicationToken(models.Model):
    name = models.CharField(max_length=250, unique=True)
    key = models.CharField(max_length=32, default=get_random_string(32), unique=True, editable=False)

    def __str__(self):
        return f'{self.name}  -  {self.key}'

    def change(self):
        self.key = get_random_string(32)