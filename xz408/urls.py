from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('econometrica', views.econometrica, name='econometrica'),
    path('developers', views.developers, name='developers'),
    path('contact', views.contact, name='contact'),
]