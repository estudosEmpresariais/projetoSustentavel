from django.contrib import admin
from django.urls import path, include
from .views import apresentation
from . import views



app_name = "usuarios"


urlpatterns = [
	path('', views.apresentation, name='apresentation'),
]

