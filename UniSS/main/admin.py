from django.contrib import admin
from .models import *

admin.site.register([ApplicationToken, Shop, ShopChain, Product])