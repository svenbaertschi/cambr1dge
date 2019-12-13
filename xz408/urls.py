from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('apps', views.apps, name='apps'),
    path('developers', views.developers, name='developers'),
    path('contact', views.contact, name='contact'),
]