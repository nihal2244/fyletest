from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('withifsc',views.getifsc,name='bankinfo'),
    path('citybranch',views.filterbyname,name='citybranch'),
    path('jwt',views.jwtGenerator,name='jwt'),
    
 
]