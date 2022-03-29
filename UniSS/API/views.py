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


def JustMessage(message, status=status.HTTP_200_OK):
    return Response({
        'message': message,
    }, status=status)


def app_permissions(func):
    def wrapper(self, request, *args, **kwargs):
        if 'App-Token' not in request.headers:
            return JustMessage("App token is empty!", status=status.HTTP_401_UNAUTHORIZED)
        elif not ApplicationToken.objects.filter(key=request.headers['App-Token']).exists():
            return JustMessage("App is not authenticated!", status=status.HTTP_401_UNAUTHORIZED)
        elif ApplicationToken.objects.get(key=request.headers['App-Token']).active == False:
            return JustMessage('App token is not active!', status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)

    return wrapper


def defaultResponse():
    return Response(None, status=status.HTTP_204_NO_CONTENT)


def exceptionResponse(e):
    return JustMessage(f'[EXCEPTION] {str(e)}', status=status.HTTP_400_BAD_REQUEST)


def user_is_authenticated(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Auth-Token' in request.headers:
            if Token.objects.filter(key=request.data['Auth-Token']).exists():
                return func(self, request, *args, **kwargs)
        return JustMessage('User is not authenticated!', status=status.HTTP_401_UNAUTHORIZED)

    return wrapper


class CreateAppToken(APIView):
    @user_is_authenticated
    def post(self, request):
        try:
            token = request.headers['Auth-Token']
            user = Token.objects.get(key=token).user
            if 'name' not in request.data:
                return JustMessage('Name is empty!', status=status.HTTP_400_BAD_REQUEST)
            name = request.data['name']
            if ApplicationToken.objects.filter(name=name).exists():
                return JustMessage('This name of token already exists!', status=status.HTTP_208_ALREADY_REPORTED)
            app_token = ApplicationToken.objects.create(name=name, creator=user)
            return JustMessage(f'Your application ({name}) has been accepted.')
        except Exception as e:
            return exceptionResponse(e)


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
                return JustMessage("Do not give a latitude and (or) a longitude!", status=status.HTTP_400_BAD_REQUEST)
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
                return JustMessage("Username is empty!", status=status.HTTP_400_BAD_REQUEST)
            username = request.data['username']
            if not User.objects.filter(username=username).exists():
                return JustMessage("User is not found!", status=status.HTTP_404_NOT_FOUND)
            if 'password' not in request.data:
                return JustMessage("Password is empty!", status=status.HTTP_400_BAD_REQUEST)
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return JustMessage("The password is incorrect!", status=status.HTTP_400_BAD_REQUEST)
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
            data['shops'] = ShopSerializer(shops, many=True).data
            if 'chain' in request.headers:
                h_chain = int(request.headers['chain'])
                if shops.filter(chain=h_chain).exists():
                    shops = shops.filter(chain=h_chain)
                    data['shops'] = ShopSerializer(shops, many=True).data
                elif not ShopChain.objects.filter(id=h_chain).exists():
                    return JustMessage("This chain of shops does not exists!", status=status.HTTP_404_NOT_FOUND)
                else:
                    return JustMessage("Shop list is empty!", status=status.HTTP_204_NO_CONTENT)
            if 'id' in request.headers:
                h_id = int(request.headers['id'])
                if shops.filter(id=h_id).exists():
                    shops = shops.get(id=h_id)
                    print(shops)
                    data['shops'] = ShopSerializer(shops).data
                    return Response(data)
                else:
                    return JustMessage("This shop does not exists!", status=status.HTTP_404_NOT_FOUND)
            if 'find' in request.GET:
                shops = shops.filter(chain__in=ShopChain.objects.filter(name__icontains=request.GET['find']))
            if shops:
                data['shops'] = data['shops']
                return Response(data)
            else:
                return JustMessage("Shop list is empty!", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.headers['Auth-Token']
            if 'chain' not in request.data:
                return JustMessage("Chain of shops is empty!", status=status.HTTP_400_BAD_REQUEST)
            if not ShopChain.objects.filter(id=int(request.data['chain'])).exists():
                return JustMessage("This chain of shops is not found!", status=status.HTTP_404_NOT_FOUND)
            chain = ShopChain.objects.get(id=int(request.data['chain']))
            if not chain.managers.filter(auth_token=token).exists():
                return JustMessage("You do not have permissions!", status=status.HTTP_403_FORBIDDEN)
            manager = Token.objects.get(key=request.data['auth_token']).user
            if 'lat' not in request.data or 'lng' not in request.data:
                return JustMessage("Do not give a latitude and (or) a longitude!",
                                   status=status.HTTP_400_BAD_REQUEST)
            lat = float(request.data['lat'])
            lng = float(request.data['lng'])
            shop = Shop.objects.create(chain=chain, lat=lat, lng=lng)
            shop.managers.add(manager)
            data['shop'] = ShopSerializer(shop).data
            data['message'] = "Shop has been created!"
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def delete(self, request):
        try:
            data = {}
            token = request.headers['Auth-Token']
            if 'id' not in request.data:
                data['message'] = "Id is empty!"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif not Shop.objects.filter(id=int(request.data['id'])).exists():
                return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
            else:
                id = int(request.data['id'])
            if not ShopChain.objects.get(id=Shop.objects.get(id=id).chain.id).managers.filter(
                    id=Token.objects.get(key=token).user.id).exists():
                return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
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
            token = request.headers['Auth-Token']
            if 'id' not in request.data:
                return JustMessage("Id is empty!", status=status.HTTP_400_BAD_REQUEST)
            elif not Shop.objects.filter(id=int(request.data['id'])).exists():
                return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
            else:
                id = int(request.data['id'])
            if not ShopChain.objects.get(id=Shop.objects.get(id=id).chain.id).managers.filter(
                    id=Token.objects.get(key=token).user.id).exists():
                return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
            shop = Shop.objects.get(id=id)
            changed = False
            if 'chain' in request.data:
                if not ShopChain.objects.filter(id=int(request.data['chain'])).exists():
                    return JustMessage("This chain does not exists!", status=status.HTTP_404_NOT_FOUND)
                if int(request.data['chain']) != int(shop.chain.id):
                    changed = True
                    shop.chain = ShopChain.objects.get(id=int(request.data['chain']))
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
                return JustMessage("No changes")
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
                return JustMessage("Select a type request!", status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.headers:
                return JustMessage("Id is empty!", status=status.HTTP_400_BAD_REQUEST)
            id = request.headers['id']
            if request.headers['type'] == 'chain':
                if ShopChain.objects.filter(id=int(id)).exists():
                    data['managers'] = ManagerSerializer(ShopChain.objects.get(id=id).managers, many=True).data
                    return Response(data)
                else:
                    return JustMessage("Chain is not found!", status=status.HTTP_404_NOT_FOUND)
            elif request.headers['type'] == 'shop':
                if Shop.objects.filter(id=int(id)).exists():
                    data['managers'] = ManagerSerializer(Shop.objects.get(id=id).managers, many=True).data
                    return Response(data)
                else:
                    return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
            else:
                return JustMessage("Type is incorrect!", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.headers['Auth-Token']
            if 'type' not in request.data:
                return JustMessage("Select a type manager!", status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.data:
                return JustMessage("Id is empty!", status=status.HTTP_400_BAD_REQUEST)
            id = int(request.data['id'])
            if 'user' not in request.data:
                return JustMessage("User is empty!", status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(id=int(request.data['user'])).exists():
                user = request.data['user']
                if request.data['type'] == 'chain':
                    if ShopChain.objects.filter(id=int(id)).exists():
                        if not ShopChain.objects.get(id=int(id)).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists():
                            return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
                        if not ShopChain.objects.get(id=int(id)).managers.filter(id=int(user)).exists():
                            ShopChain.objects.get(id=int(id)).managers.add(User.objects.get(id=int(user)))
                            data['message'] = "Manager has been added!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=int(user))).data
                            return Response(data)
                        else:
                            return JustMessage("User is already a manager in this chain!",
                                               status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        return JustMessage("Chain is not found!", status=status.HTTP_404_NOT_FOUND)
                elif request.data['type'] == 'shop':
                    if Shop.objects.filter(id=id).exists():
                        if not Shop.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists() and not ShopChain.objects.get(
                            id=Shop.objects.get(id=id).chain.id).managers.filter(
                            id=Token.objects.get(key=token).user.id).exists():
                            return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
                        if not Shop.objects.get(id=int(id)).managers.filter(id=int(user)).exists():
                            Shop.objects.get(id=int(id)).managers.add(User.objects.get(id=int(user)))
                            data['message'] = "Manager has been added!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=int(user))).data
                            return Response(data)
                        else:
                            return JustMessage("User is already a manager in this shop!",
                                               status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
                else:
                    return JustMessage("Type is incorrect!", status=status.HTTP_400_BAD_REQUEST)
            else:
                return JustMessage("User is not found!", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()

    @app_permissions
    @user_is_authenticated
    def delete(self, request):
        try:
            data = {}
            token = request.headers['Auth-Token']
            if 'type' not in request.data:
                return JustMessage("Select a type manager!", status=status.HTTP_400_BAD_REQUEST)
            elif 'id' not in request.data:
                return JustMessage("Id is empty!", status=status.HTTP_400_BAD_REQUEST)
            id = int(request.data['id'])
            if 'user' not in request.data:
                return JustMessage("User is empty!", status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(id=int(request.data['user'])).exists():
                user = int(request.data['user'])
                if request.data['type'] == 'chain':
                    if ShopChain.objects.filter(id=id).exists():
                        if not ShopChain.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists():
                            return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
                        if ShopChain.objects.get(id=id).managers.filter(id=user).exists():
                            ShopChain.objects.get(id=id).managers.remove(User.objects.get(id=user))
                            data['message'] = "Manager has been removed!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=user)).data
                            return Response(data)
                        else:
                            return JustMessage("User is not a manager in this chain!",
                                               status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        return JustMessage("Chain is not found!", status=status.HTTP_404_NOT_FOUND)
                elif request.data['type'] == 'shop':
                    if Shop.objects.filter(id=id).exists():
                        if not Shop.objects.get(id=id).managers.filter(
                                id=Token.objects.get(key=token).user.id).exists() and not ShopChain.objects.get(
                            id=Shop.objects.get(id=id).chain.id).managers.filter(
                            id=Token.objects.get(key=token).user.id).exists():
                            return JustMessage("You do not have a permissions!", status=status.HTTP_403_FORBIDDEN)
                        if Shop.objects.get(id=id).managers.filter(id=user).exists():
                            Shop.objects.get(id=id).managers.remove(User.objects.get(id=user))
                            data['message'] = "Manager has been deleted!"
                            data['manager'] = ManagerSerializer(User.objects.get(id=user)).data
                            return Response(data)
                        return JustMessage("User is not a manager in this shop!",
                                           status=status.HTTP_208_ALREADY_REPORTED)
                    else:
                        return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
                else:
                    return JustMessage("Type is incorrect!", status=status.HTTP_400_BAD_REQUEST)
            else:
                return JustMessage("User is not found!", status=status.HTTP_400_BAD_REQUEST)
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
            if 'shop' in request.headers:
                shop_id = int(request.headers['shop'])
                if not Shop.objects.filter(id=shop_id).exists():
                    return JustMessage("This shop is not found!", status=status.HTTP_404_NOT_FOUND)
                products = products.filter(shop=Shop.objects.get(id=shop_id))
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
            token = request.headers['Auth-Token']
            user = Token.objects.get(key=token).user
            if 'shop' not in request.data:
                return JustMessage('Shop id is empty!', status=status.HTTP_400_BAD_REQUEST)
            if not Shop.objects.filter(id=int(request.data['shop'])).exists():
                return JustMessage("Shop is not found!", status=status.HTTP_404_NOT_FOUND)
            shop = Shop.objects.get(id=int(request.data['shop']))
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
            token = request.headers['Auth-Token']
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
            token = request.headers['Auth-Token']
            user = Token.objects.get(key=token).user
            if 'id' not in request.data:
                return JustMessage('Id is empty!', status=status.HTTP_400_BAD_REQUEST)
            id = int(request.data['id'])
            if not Product.objects.filter(id=id).exists():
                return JustMessage('This product is not found!', status=status.HTTP_404_NOT_FOUND)
            shop = Product.objects.get(id=id).shop
            product = Product.objects.get(id=id)
            if not shop.managers.filter(id=user.id).exists():
                return JustMessage('You do not have permissions!', status=status.HTTP_403_FORBIDDEN)
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


class AddCountProductView(APIView):
    @app_permissions
    @user_is_authenticated
    def post(self, request):
        try:
            data = {}
            token = request.headers['Auth-Token']
            user = Token.objects.get(key=token).user
            if 'id' not in request.data:
                return JustMessage('Id is empty!', status=status.HTTP_400_BAD_REQUEST)
            id = int(request.data['id'])
            if not Product.objects.filter(id=id).exists():
                return JustMessage('This product is not found!', status=status.HTTP_404_NOT_FOUND)
            shop = Product.objects.get(id=id).shop
            product = Product.objects.get(id=id)
            if not shop.managers.filter(id=user.id).exists():
                return JustMessage('You do not have permissions!', status=status.HTTP_403_FORBIDDEN)
            if 'count' not in request.data:
                return JustMessage('Count is empty!', status=status.HTTP_400_BAD_REQUEST)
            count = int(request.data['count'])
            change = product.change_count(count)
            if change == None:
                return JustMessage('Some error with add to count!', status=status.HTTP_400_BAD_REQUEST)
            data['message'] = "Count has been added successfully!"
            data['product'] = ProductSerializer(product).data
            product.save()
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class ChainsView(APIView):
    @app_permissions
    def get(self, request):
        try:
            chains = ShopChain.objects.all()
            data = {
                'chains': ShopChainSerializer(chains, many=True).data
            }
            if 'id' in request.headers:
                if chains.filter(id=int(request.headers['id'])).exists():
                    chains = chains.get(id=int(request.headers['id']))
                    data['chains'] = ShopChainSerializer(chains).data
                    return Response(data)
                else:
                    return JustMessage('This chain is not found!', status=status.HTTP_404_NOT_FOUND)
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class UserView(APIView):
    @app_permissions
    def get(self, request):
        try:
            if 'Auth-Token' not in request.headers:
                return JustMessage('Auth-Token is empty!', status=status.HTTP_400_BAD_REQUEST)
            if not Token.objects.filter(key=request.headers['Auth-Token']).exists():
                return JustMessage('Wrong token!', status=status.HTTP_401_UNAUTHORIZED)
            auth_token = request.headers['Auth-Token']
            user = Token.objects.get(key=auth_token).user
            data = {
                'user': UserSerializer(user).data,
            }
            return Response(data)
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()


class GetShopNameView(APIView):
    @app_permissions
    def get(self, request):
        try:
            data = {}
            if 'product' not in request.headers and 'shop' not in request.headers:
                return JustMessage('Product or shop id is empty!', status=status.HTTP_400_BAD_REQUEST)
            if 'product' in request.headers:
                product_id = int(request.headers['product'])
                if Product.objects.filter(id=product_id).exists():
                    data['shop_name'] = Product.objects.get(id=product_id).shop.chain.name
                    return Response(data)
                else:
                    return JustMessage('This product is not found!')
            if 'shop' in request.headers:
                shop_id = int(request.headers['shop'])
                if Shop.objects.filter(id=shop_id).exists():
                    data['shop_name'] = Shop.objects.get(id=shop_id).chain.name
                    return Response(data)
                else:
                    return JustMessage('This shop is not found!')
        except Exception as e:
            return exceptionResponse(e)
        return defaultResponse()
