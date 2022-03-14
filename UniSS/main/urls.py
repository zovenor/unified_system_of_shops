from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.ShopsView.as_view()),
    path('chains/', views.ChainsView.as_view()),
]
