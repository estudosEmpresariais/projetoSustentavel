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
	path('detail_empreendedor/<int:usuario_id>/<int:pk>', views.detail_empreendedor.as_view(), name='detail_empreendedor'),
	path('edicao_user/<int:usuario_id>', views.edicao_user.as_view(), name='edicao_user'),
	path('editar_user/<int:usuario_id>', views.editar_user, name='editar_user'),
]

