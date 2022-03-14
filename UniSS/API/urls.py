from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', views.TokenView.as_view()),
    path('shops_around/', views.get_shops_around_api),
    path('shops/', views.ShopsView.as_view()),
    path('create_shop', views.CreateShopView.as_view()),
]
