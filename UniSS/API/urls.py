from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', views.TokenView.as_view()),
    path('create_app_token/', views.CreateAppToken.as_view()),
    path('shops_around/', views.GetShopAroundView.as_view()),
    path('shops/', views.ShopsView.as_view()),
    path('managers/', views.ManagersView.as_view()),
    path('products/', views.ProductsView.as_view()),
    path('products/add_count/', views.AddCountProductView.as_view()),
    path('chains/', views.ChainsView.as_view()),
    path('user/', views.UserView.as_view()),
    path('get_shop_name/', views.GetShopNameView.as_view()),
    path('get_product_by_code/', views.GetProductByCodeView.as_view()),
    path('register/', views.RegisterUserView.as_view()),
]
