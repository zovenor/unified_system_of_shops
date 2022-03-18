from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .algoritms import *
from .models import ApplicationToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from main.models import Shop, ShopChain, Product
from .serializers import ShopSerializer, ShopChainSerializer, UserSerializer, ManagerSerializer, ProductSerializer


def app_permissions(func):
    def wrapper(self, request, *args, **kwargs):
        if 'app_token' not in request.data:
            return Response({
                'message': "App is not authenticated!",
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif not ApplicationToken.objects.filter(key=request.data['app_token']).exists():
            return Response({
                'message': "App is not authenticated!",
            }, status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)

    return wrapper


def JustMessage(message, status=status.HTTP_200_OK):
    return Response({
        'message': message,
    }, status=status)


def defaultResponse():
    return Response(None, status=status.HTTP_204_NO_CONTENT)


def exceptionResponse(e):
    return Response({
        'message ': f'[EXCEPTION] {str(e)}',
    }, status=status.HTTP_400_BAD_REQUEST)


def user_is_authenticated(func):
    def wrapper(self, request, *args, **kwargs):
        if 'auth_token' in request.data:
            if Token.objects.filter(key=request.data['auth_token']).exists():
                return func(self, request, *args, **kwargs)
        return Response({
            'message': 'User is not authenticated!',
        }, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper


class GetShopAroundView(APIView):
    @app_permissions
    def get(self, request):
        try:
            data = {}
            shops = None
            data['shops'] = shops
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
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class TokenView(APIView):
    @app_permissions
    def post(self, request):
        try:
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
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class ShopsView(APIView):
    @app_permissions
    def get(self, request):
        try:
            data = {}
            shops = Shop.objects.all()
            data['shops'] = ShopSerializer(shops, many=True)
            if 'chain' in request.headers:
                h_chain = int(request.headers['chain'])
                if shops.filter(chain=h_chain).exists():
                    shops = shops.filter(chain=h_chain)
                    data['shops'] = ShopSerializer(shops, many=True).data
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
                    data['shops'] = ShopSerializer(shops).data
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
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            if 'chain' in request.data:
                chain_id = int(request.data['chain'])
                if ShopChain.objects.filter(id=chain_id).exists():
                    chain = ShopChain.objects.get(id=chain_id)
                    if chain.managers.filter(auth_token=token).exists():
                        data['message'] = "Shop has been created!"
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
                        data['message'] = "Shop has been created!"
                        return Response(data)
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
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def delete(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            id = None
            if 'id' not in request.headers:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif not Shop.objects.filter(id=int(request.headers['id'])).exists():
                data['message'] = "Shop is not found!"
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                id = int(request.headers['id'])
            if not ShopChain.objects.get(id=Shop.objects.get(id=id).chain.id).managers.filter(
                    id=Token.objects.get(key=token).user.id).exists():
                data['message'] = "You do not have a permissions!"
                return Response(data, status=status.HTTP_403_FORBIDDEN)
            Shop.objects.get(id=id).delete()
            data['message'] = "Shop has been deleted!"
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def patch(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            id = None
            if 'id' not in request.headers:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif not Shop.objects.filter(id=int(request.headers['id'])).exists():
                data['message'] = "Shop is not found!"
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                id = int(request.headers['id'])
            if not ShopChain.objects.get(id=Shop.objects.get(id=id).chain.id).managers.filter(
                    id=Token.objects.get(key=token).user.id).exists():
                data['message'] = "You do not have a permissions!"
                return Response(data, status=status.HTTP_403_FORBIDDEN)
            shop = Shop.objects.get(id=id)
            changed = False
            if 'chain' in request.data:
                if ShopChain.objects.filter(id=int(request.data['chain'])).exists():
                    if int(request.data['chain']) != int(shop.chain.id):
                        changed = True
                        shop.chain = ShopChain.objects.get(id=int(request.data['chain']))
                else:
                    data['message'] = "This chain does not exists!"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
            if 'lat' in request.data:
                if float(request.data['lat']) != shop.lat:
                    changed = True
                    shop.lat = float(request.data['lat'])
            if 'lng' in request.data:
                if float(request.data['lng']) != shop.lng:
                    changed = True
                    shop.lng = float(request.data['lng'])
            if changed:
                shop.save()
                data['message'] = "Shop has been updated!"
                data['shop'] = ShopSerializer(shop).data
            else:
                data['message'] = "No changes"
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class ManagersView(APIView):
    @app_permissions
    @user_is_authenticated
    def get(self, request):
        try:
            data = {}
            if 'type' not in request.headers:
                data['message'] = "Select a type request!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.headers:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            id = request.headers['id']
            if request.headers['type'] == 'chain':
                if ShopChain.objects.filter(id=int(id)).exists():
                    data['managers'] = ManagerSerializer(ShopChain.objects.get(id=id).managers, many=True).data
                    return Response(data)
                else:
                    data['message'] = "Chain is not found!"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
            elif request.headers['type'] == 'shop':
                if Shop.objects.filter(id=int(id)).exists():
                    data['managers'] = ManagerSerializer(Shop.objects.get(id=id).managers, many=True).data
                    return Response(data)
                else:
                    data['message'] = "Shop is not found!"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                data['message'] = "Type is incorrect!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            if 'type' not in request.headers:
                data['message'] = "Select a type manager!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.headers:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            id = int(request.headers['id'])
            if 'user' not in request.data:
                data['message'] = "User is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(id=int(request.data['user'])).exists():
                user = request.data['user']
                if request.headers['type'] == 'chain':
                    if ShopChain.objects.filter(id=int(id)).exists():
                        if not ShopChain.objects.get(id=int(id)).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists():
                            data['message'] = "You do not have a permissions!"
                            return Response(data, status=status.HTTP_403_FORBIDDEN)
                        if not ShopChain.objects.get(id=int(id)).managers.filter(id=int(user)).exists():
                            ShopChain.objects.get(id=int(id)).managers.add(User.objects.get(id=int(user)))
                            data['message'] = "Manager has been added!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=int(user))).data
                            return Response(data)
                        else:
                            data['message'] = "User is already a manager in this chain!"
                            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        data['message'] = "Chain is not found!"
                        return Response(data, status=status.HTTP_404_NOT_FOUND)
                elif request.headers['type'] == 'shop':
                    if Shop.objects.filter(id=id).exists():
                        if not Shop.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists() and not ShopChain.objects.get(
                            id=Shop.objects.get(id=id).chain.id).managers.filter(
                            id=Token.objects.get(key=token).user.id).exists():
                            data['message'] = "You do not have a permissions!"
                            return Response(data, status=status.HTTP_403_FORBIDDEN)
                        if not Shop.objects.get(id=int(id)).managers.filter(id=int(user)).exists():
                            Shop.objects.get(id=int(id)).managers.add(User.objects.get(id=int(user)))
                            data['message'] = "Manager has been added!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=int(user))).data
                            return Response(data)
                        else:
                            data['message'] = "User is already a manager in this shop!"
                            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        data['message'] = "Shop is not found!"
                        return Response(data, status=status.HTTP_404_NOT_FOUND)
                else:
                    data['message'] = "Type is incorrect!"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['message'] = "User is not found!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def delete(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            if 'type' not in request.headers:
                data['message'] = "Select a type manager!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.headers:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            id = int(request.headers['id'])
            if 'user' not in request.data:
                data['message'] = "User is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(id=int(request.data['user'])).exists():
                user = int(request.data['user'])
                if request.headers['type'] == 'chain':
                    if ShopChain.objects.filter(id=id).exists():
                        if not ShopChain.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists():
                            data['message'] = "You do not have a permissions!"
                            return Response(data, status=status.HTTP_403_FORBIDDEN)
                        if ShopChain.objects.get(id=id).managers.filter(id=user).exists():
                            ShopChain.objects.get(id=id).managers.remove(User.objects.get(id=user))
                            data['message'] = "Manager has been removed!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=user)).data
                            return Response(data)
                        else:
                            data['message'] = "User is not a manager in this chain!"
                            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        data['message'] = "Chain is not found!"
                        return Response(data, status=status.HTTP_404_NOT_FOUND)
                elif request.headers['type'] == 'shop':
                    if Shop.objects.filter(id=id).exists():
                        if not Shop.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists() and not ShopChain.objects.get(
                            id=Shop.objects.get(id=id).chain.id).managers.filter(
                            id=Token.objects.get(key=token).user.id).exists():
                            data['message'] = "You do not have a permissions!"
                            return Response(data, status=status.HTTP_403_FORBIDDEN)
                        if Shop.objects.get(id=id).managers.filter(id=user).exists():
                            Shop.objects.get(id=id).managers.remove(User.objects.get(id=user))
                            data['message'] = "Manager has been deleted!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=user)).data
                            return Response(data)
                        data['message'] = "User is not a manager in this shop!"
                        return Response(data, status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        data['message'] = "Shop is not found!"
                        return Response(data, status=status.HTTP_404_NOT_FOUND)
                else:
                    data['message'] = "Type is incorrect!"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['message'] = "User is not found!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class ProductsView(APIView):
    @app_permissions
    def get(self, request):
        try:
            products = Product.objects.all()
            data = {}
            if 'chain' in request.headers:
                chain_id = int(request.headers['chain'])
                if products_in_chain_of_shops(chain_id) == None:
                    data['message'] = "This chain is not found!"
                    return Response(data, status=status.HTTP_404_NOT_FOUND)
                products = products.filter(shop__in=products_in_chain_of_shops(chain_id))
            if 'id' in request.headers:
                product_id = int(request.headers['id'])
                if not Product.objects.filter(id=product_id).exists():
                    return JustMessage("This product is not found!", status=status.HTTP_404_NOT_FOUND)
                products = products.filter(id=product_id)
            if 'find' in request.GET:
                products = products.filter(name__icontains=request.GET['find'])
            data['products'] = ProductSerializer(products, many=True).data
            return Response(data)

        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            user = Token.objects.get(key=token).user
            if 'shop' not in request.headers:
                return JustMessage('Shop id is empty!', status=status.HTTP_400_BAD_REQUEST)
            if not Shop.objects.filter(id=int(request.headers['shop'])).exists():
                return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
            shop = Shop.objects.get(id=int(request.headers['shop']))
            if not shop.managers.filter(id=user.id).exists() and not shop.chain.managers.filter(id=user.id):
                return JustMessage("You do not have permissions!")
            if 'name' not in request.data:
                return JustMessage("Name is empty!", status=status.HTTP_400_BAD_REQUEST)
            if 'price' not in request.data:
                return JustMessage("Price is empty!", status=status.HTTP_400_BAD_REQUEST)
            if 'currency' not in request.data:
                return JustMessage("Currency is empty!", status=status.HTTP_400_BAD_REQUEST)
            if 'count' not in request.data:
                return JustMessage("Count is empty!", status=status.HTTP_400_BAD_REQUEST)
            if 'code' not in request.data:
                return JustMessage("Code is empty!", status=status.HTTP_400_BAD_REQUEST)
            name = request.data['name']
            price = float(request.data['price'])
            currency = request.data['currency']
            count = int(request.data['count'])
            code = int(request.data['code'])
            product = Product.objects.create(name=name, price=price, currency=currency, count=count, code=code,
                                             shop=shop)
            data['message'] = "Product has been added successfully!"
            data['product'] = ProductSerializer(product).data
            return Response(data)

        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def delete(self, request):
        try:
            token = request.data['auth_token']
            user = Token.objects.get(key=token).user
            if 'id' not in request.data:
                return JustMessage('Id is empty!', status=status.HTTP_400_BAD_REQUEST)
            id = int(request.data['id'])
            if not Product.objects.filter(id=id).exists():
                return JustMessage('This product is not found!')
            shop = Product.objects.get(id=id).shop
            product = Product.objects.get(id=id)
            if not shop.managers.filter(id=user.id).exists():
                return JustMessage('You do not have permissions!')
            product.delete()
            return JustMessage('Product has been deleted successfully!')
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def patch(self, request):
        try:
            data = {}
            token = request.data['auth_token']
            user = Token.objects.get(key=token).user
            if 'id' not in request.headers:
                return JustMessage('Id is empty!', status=status.HTTP_400_BAD_REQUEST)
            id = int(request.headers['id'])
            if not Product.objects.filter(id=id).exists():
                return JustMessage('This product is not found!')
            shop = Product.objects.get(id=id).shop
            product = Product.objects.get(id=id)
            if not shop.managers.filter(id=user.id).exists():
                return JustMessage('You do not have permissions!')
            changed = False
            if 'name' in request.data:
                product.name = request.data['name']
                changed = True
            if 'price' in request.data:
                product.price = float(request.data['price'])
                changed = True
            if 'currency' in request.data:
                product.currency = request.data['currency']
                changed = True
            if 'count' in request.data:
                product.count = int(request.data['count'])
                changed = True
            if 'code' in request.data:
                product.code = int(request.data['code'])
                changed = True
            if 'shop' in request.data:
                product.shop = int(request.data['shop'])
                changed = True
            if changed:
                product.save()
                data['message'] = "Product has been updated successfully!"
                data['product'] = ProductSerializer(product).data
                return Response(data)
            else:
                return JustMessage('No changes')

        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()
