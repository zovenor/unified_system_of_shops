from django.urls import path
from . import views

urlpatterns = [
    path('shops_around', views.get_shops_around_api),
]
