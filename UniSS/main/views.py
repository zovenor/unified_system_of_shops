from django.shortcuts import render
from django.views import View
from .models import *
from django.conf import settings


class ShopsView(View):
    def get(self, request):
        data = {
            'shops': Shop.objects.all(),
            'mapbox_token': settings.MAPBOX_TOKEN,
        }

        if 'chain' in request.GET:
            data['shops'] = data['shops'].filter(chain=ShopChain.objects.get(unique_name=request.GET['chain']))

        return render(request, 'main/shops.html', data)


class ChainsView(View):
    def get(self, request):
        data = {
            'chains': ShopChain.objects.all(),
        }

        return render(request, 'main/chains.html', data)
