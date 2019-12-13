from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.stocks, name='stocks'),
    path('weather', views.weather, name='weather'),
]