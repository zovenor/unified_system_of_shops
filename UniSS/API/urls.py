from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', views.TokenView.as_view()),
    path('shops_around/', views.GetShopAroundView.as_view()),
    path('shops/', views.ShopsView.as_view()),
    path('managers/', views.ManagersView.as_view()),
    path('products/', views.ProductsView.as_view()),
    path('products/add_count/', views.AddCountProductView.as_view()),
]
