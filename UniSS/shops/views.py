from django.shortcuts import render
from django.views import View
from .models import Shop
from django.conf import settings


class IndexView(View):
    def get(self, request):
        content = {
            'shop': Shop.objects.get(id=1),
            'mapbox_token': settings.LOCATION_FIELD['provider.mapbox.access_token'],
        }

        print(content['shop'])

        return render(request, 'shops/index.html', content)
