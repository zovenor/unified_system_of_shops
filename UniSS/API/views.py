from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from main.models import Shop
from .serializers import ShopSerializer
import json
from .algoritms import *


@api_view(['GET'])
def get_shops_around_api(request):
    shops = None

    try:
        if 'lat' in request.GET and 'lng' in request.GET:
            shops = ShopSerializer(get_shops_around([int(request.GET['lat']), int(request.GET['lng'])]), many=True).data
    except:
        pass

    return Response({
        'shops': shops,
    })
