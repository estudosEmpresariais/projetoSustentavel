from django.contrib import admin
from django.urls import path, include
from .views import apresentation
from . import views



app_name = "usuarios"


urlpatterns = [
	path('', views.apresentation, name='apresentation'),
	path('login/', views.login, name='login'),
	path('registro/', views.registro, name='registro'),
	path('create/', views.create_user, name='create_user'),
	path('empreendedores/<int:id>', views.empreendedores.as_view(), name='empreendedores'),
	path('logar/', views.logar, name='logar'),
	path('sobre/', views.sobre, name='sobre'),
	path('detail_empreendedor/<int:pk>', views.detail_empreendedor.as_view(), name='detail_empreendedor'),
]

