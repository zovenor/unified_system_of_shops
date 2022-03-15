from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from main.models import Shop, ShopChain
from .serializers import ShopSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from .algoritms import *


def user_is_authenticated(func):
    def wrapper(self, request, *args, **kwargs):
        if 'auth_token' in request.data:
            if Token.objects.filter(key=request.data['auth_token']).exists():
                return func(self, request, *args, **kwargs)
        return Response({
            'message': 'User is not authenticated!',
        }, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper


def create_shop(request, data):
    try:
        chain = ShopChain.objects.get(id=int(request.data['chain']))
        manager = Token.objects.get(key=request.data['auth_token']).user
        if 'lat' in request.data and 'lng' in request.data:
            lat = float(request.data['lat'])
            lng = float(request.data['lng'])
        else:
            data['message'] = "Do not give a latitude and (or) a longitude!"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        shop = Shop.objects.create(chain=chain, lat=lat, lng=lng)
        shop.managers.add(manager)
        data['shop'] = ShopSerializer(shop).data
        return Response(data)
    except Exception as e:
        data['message'] = f'[EXCEPTION] {str(e)}'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_shops_around_api(request):
    shops = None

    data = {
        'shops': shops,
    }

    try:
        if 'lat' in request.headers and 'lng' in request.headers:
            shops = ShopSerializer(get_shops_around([float(request.headers['lat']), float(request.headers['lng'])]),
                                   many=True).data
            data['shops'] = shops
        else:
            del data['shops']
            data['message'] = "Do not give a latitude and (or) a longitude!"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if 'radius' in request.headers:
            shops = ShopSerializer(get_shops_around([float(request.headers['lat']), float(request.headers['lng'])],
                                                    radius=float(request.headers['radius'])), many=True).data
            data['shops'] = shops
    except Exception as e:
        data['message'] = f'[EXCEPTION] {str(e)}'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)


class TokenView(APIView):
    def post(self, request):
        data = {}

        if 'username' not in request.data:
            data['message'] = "Username is empty!"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            username = request.data['username']
            if not User.objects.filter(username=username).exists():
                data['message'] = "User is not found!"
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        if 'password' not in request.data:
            data['message'] = "Password is empty!"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                data['message'] = "The password is incorrect!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['token'] = Token.objects.get_or_create(user=user)[0].key

        return Response(data)


class ShopsView(APIView):
    def get(self, request):

        shops = Shop.objects.all()

        data = {
            'shops': ShopSerializer(shops, many=True),
        }

        try:
            if 'chain' in request.headers:
                h_chain = int(request.headers['chain'])
                if shops.filter(chain=h_chain).exists():
                    shops = shops.filter(chain=h_chain)
                    data['shops'] = ShopSerializer(shops, many=True)
                elif not ShopChain.objects.filter(id=h_chain).exists():
                    data['message'] = "This chain of shops does not exists!"
                    del shops
                    del data['shops']
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
                else:
                    data['message'] = "Shop list is empty!"
                    del shops
                    del data['shops']
                    return Response(data, status=status.HTTP_204_NO_CONTENT)

            if 'id' in request.headers:
                h_id = int(request.headers['id'])
                if shops.filter(id=h_id).exists():
                    shops = shops.get(id=h_id)
                    data['shops'] = ShopSerializer(shops)
                else:
                    data['message'] = "This shop does not exists!"
                    del shops
                    del data['shops']
                    return Response(data, status=status.HTTP_404_NOT_FOUND)

            if shops:
                data['shops'] = data['shops'].data
            else:
                del data['shops']
                del shops
                data['message'] = "Shop list is empty!"
                return Response(data, status=status.HTTP_204_NO_CONTENT)

            return Response(data)
        except Exception as e:
            del data['shops']
            data['message'] = f'[EXCEPTION] {str(e)}'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @user_is_authenticated
    def post(self, request):
        token = request.data['auth_token']
        data = {}

        try:
            if 'chain' in request.data:
                chain = int(request.data['chain'])
                if ShopChain.objects.filter(id=chain).exists():
                    chain = ShopChain.objects.get(id=chain)
                    if chain.managers.filter(auth_token=token).exists():
                        data['message'] = "Shop has been created!"
                        return create_shop(request, data)
                    else:
                        data['message'] = "You do not have a permissions!"
                        return Response(data, status=status.HTTP_403_FORBIDDEN)
                else:
                    data['message'] = "This chain is not defined!"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                data['message'] = "Select a chain of shops!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data['message'] = f'[EXCEPTION] {str(e)}'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @user_is_authenticated
    def delete(self, request):
        token = request.data['auth_token']
        data = {}

        try:
            id = None
            if 'id' not in request.data:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif not Shop.objects.filter(id=int(request.data['id'])).exists():
                data['message'] = "Shop is not found!"
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                id = int(request.data['id'])
            if  not Shop.objects.get(id=id).managers.filter(id=Token.objects.get(key=token).user.id).exists():
                data['message'] = "You do not have a permissions!"
                return Response(data, status=status.HTTP_403_FORBIDDEN)
            Shop.objects.get(id=id).delete()
            data['message'] = "Shop has been deleted!"
            return Response(data)
        except Exception as e:
            data['message'] = f'[EXCEPTION] {e}'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
