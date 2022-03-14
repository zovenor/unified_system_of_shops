from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from main.models import Shop, ShopChain
from .serializers import ShopSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .algoritms import *


def user_is_authenticated(func):
    def wrapper(self, request, *args, **kwargs):
        if 'auth_token' in request.data:
            if Token.objects.filter(key=request.data['auth_token']).exists():
                return func(self, request, *args, **kwargs)
        return Response({
            'message': 'User is not authenticated!',
        })

    return wrapper


@api_view(['GET'])
def get_shops_around_api(request):
    shops = None

    try:
        if 'lat' in request.headers and 'lng' in request.headers:
            shops = ShopSerializer(get_shops_around([int(request.headers['lat']), int(request.headers['lng'])]),
                                   many=True).data
        if 'radius' in request.headers:
            shops = ShopSerializer(get_shops_around([int(request.headers['lat']), int(request.headers['lng'])],
                                                    radius=int(request.headers['radius'])), many=True).data
    except:
        pass

    return Response(shops)


class ShopsView(APIView):
    def get(self, request):

        shops = Shop.objects.all()

        data = {
            'message': "OK",
            'shops': ShopSerializer(shops, many=True),
        }

        try:
            if 'chain' in request.headers:
                h_chain = int(request.headers['chain'])
                if shops.filter(chain=h_chain).exists():
                    shops = shops.filter(chain=h_chain)
                    data['shops'] = ShopSerializer(shops, many=True)
                else:
                    data['message'] = "This chain of shops does not exists!"
                    del data['shops']
                    return Response(data)

            if 'id' in request.headers:
                h_id = int(request.headers['id'])
                if shops.filter(id=h_id).exists():
                    shops = shops.get(id=h_id)
                    data['shops'] = ShopSerializer(shops)
                else:
                    data['message'] = "This shop does not exists!"
                    del data['shops']
                    return Response(data)

            if shops.exists():
                data['shops'] = data['shops'].data
            else:
                del data['shops']
                del shops
                data['message'] = "Shop list is empty!"

            return Response(data)
        except:
            del data['shops']
            data['message'] = "Some error!"
            return Response(data)


class TokenView(APIView):
    def post(self, request):
        data = {
            'message': 'OK',
        }

        if 'username' not in request.data:
            data['message'] = "Username is empty!"
            return Response(data)
        else:
            username = request.data['username']
            if not User.objects.filter(username=username).exists():
                data['message'] = "User is not found!"
                return Response(data)
        if 'password' not in request.data:
            data['message'] = "Password is empty!"
            return Response(data)
        else:
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                data['message'] = "The password is incorrect!"
            else:
                data['token'] = Token.objects.get_or_create(user=user)[0].key

        return Response(data)


class CreateShopView(APIView):
    @user_is_authenticated
    def post(self, request, message='OK'):

        token = request.data['token']

        data = {
            'message': message,
        }

        if 'chain' in request.data:
            chain = int(request.data['chain'])
            if ShopChain.objects.filter(id=chain).exitst():
                chain = ShopChain.objects.get(id=chain)
                if chain.mamagers.filter(user=Token.objects.get(key=token).user).exists():
                    pass
                    # Create new shop
                else:
                    data['message'] = "User do not have a permissions for create new shop!"
                    return Response(data)
            else:
                data['message'] = "This chain is not defined!"
                return Response(data)
        else:
            data['message'] = "Select a chain of shops!"
            return Response(data)
