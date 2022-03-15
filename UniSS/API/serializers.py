from rest_framework import serializers
from main.models import Shop, ShopChain
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = '__all__'
        exclude = ['password']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopChain
        fields = '__all__'
