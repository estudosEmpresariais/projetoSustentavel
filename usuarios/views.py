from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Prefetch
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from itertools import groupby
from cadastros.city import CITIES_CHOICES
from urllib.parse import urlencode
from .models import Usuario
from cadastros.models import Pessoa, Cliente, Empreendedor, Endereco
from django.urls import reverse
from django.db.models.aggregates import Avg, Sum, Count, Min, Max
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def editar_user(request, usuario_id):
	print(f'requests: {request.POST}')
	senha = request.POST.get('senha')
	usuario = request.POST.get('usuario')
	razao_social = request.POST.get('razao_social')
	nome_fantasia = request.POST.get('nome_fantasia') 
	cidade = request.POST.get('cidade') 
	bairro = request.POST.get('bairro') if request.POST.get('bairro') else ''
	logradouro = request.POST.get('logradouro') if request.POST.get('logradouro') else ''
	numero = request.POST.get('numero') if request.POST.get('numero') else None
	complemento = request.POST.get('complemento') if request.POST.get('complemento') else ''
	cnpj = request.POST.get('cnpj')
	insc_estadual = request.POST.get('ins_estadual') if request.POST.get('ins_estadual') != '' else None
	cpf = request.POST.get('cpf') 
	descricao_servicos = request.POST.get('descricao_servicos') 
	data_nascimento = request.POST.get('data_nascimento')
	nome = request.POST.get('pessoa') if request.POST.get('pessoa') else ''
	print(f'nome:{nome}')
	email = request.POST.get('email') if request.POST.get('email') else ''
	telefone = request.POST.get('telefone') if request.POST.get('telefone') != '' else None
	foto = request.FILES.get('foto') if request.POST.get('foto') else ''
	user = Usuario.objects.filter(id=usuario_id)	
	object_user = Usuario.objects.get(id=usuario_id)	
	tipo_usuario = object_user.tipo_usuario
	username = Usuario.objects.filter(username=usuario).values('username').exclude(id=usuario_id).count()  if Usuario.objects.filter(username=usuario).values('username').count() > 0 else 0

	if username == 0:
		#user = user.update(nome=nome, senha=senha, username=usuario, password=senha, email=email)
		object_user.nome = nome
		if senha != '':
			object_user.senha = senha
			#object_user.password = object_user.set_password(senha)
		if usuario != '':
			object_user.username = usuario
		object_user.email = email
		object_user.save()
		endereco = Endereco.objects.filter(usuario__id=usuario_id)
		if endereco.count() > 0:
			endereco = Endereco.objects.get(usuario__id=usuario_id)
			endereco.bairro = bairro
			endereco.logradouro = logradouro
			endereco.numero = numero
			endereco.complemento = complemento
			endereco.usuario = object_user
			endereco.cidade = cidade
			endereco.save()
			#endereco = endereco.update(bairro=bairro, logradouro=logradouro, numero=numero, complemento=complemento, usuario=usuario_id)
			print("atualizando endereço")
		else:
			endereco = Endereco.objects.create(bairro=bairro, logradouro=logradouro, numero=numero, complemento=complemento, usuario=object_user)
			
		#user = Usuario.objects.filter(id=usuario_id)
		if tipo_usuario == 'E':
			empreendedor = Empreendedor.objects.get(usuario__id=usuario_id)
			empreendedor.razao_social = razao_social
			empreendedor.nome_fantasia = nome_fantasia
			empreendedor.cnpj = cnpj
			empreendedor.inscricao_estadual = insc_estadual
			empreendedor.telefone = telefone
			empreendedor.email = email
			empreendedor.descricao_servicos = descricao_servicos
			empreendedor.save()
			#empresa = Empreendedor.objects.update(razao_social=razao_social, nome_fantasia=nome_fantasia, cnpj=cnpj, inscricao_estadual=insc_estadual, telefone=telefone)
		else:
			cliente = Cliente.objects.get(usuario__id=usuario_id)
			cliente.nome = nome
			cliente.cpf = cpf
			cliente.data_nascimento = data_nascimento
			cliente.email = email
			cliente.telefone = telefone
			cliente.save()
			#cliente = Cliente.objects.update(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, telefone=telefone)
		mensagem = f"Usuário {usuario} atualizado com sucesso!"
		status = "sucess"
		query = urlencode({'id': object_user.id, 'usuario': object_user.username, 'status': status, 'mensagem':mensagem})
		url = reverse('usuarios:empreendedores', args=[object_user.id]) + '?' + query
		return redirect(url)

	url = reverse('usuarios:edicao_user', args=[usuario_id])
	mensagem = "O usuário enviado já existe ou alguns dados estão inconsistentes!"
	return redirect(url, usuario_id)



class edicao_user(ListView):
	model = Usuario
	template_name = 'editar_perfil.html'
	def get_context_data(self, **kwargs):
	
		try:
			endereco = Endereco.objects.get(usuario__id=self.kwargs['usuario_id'])
		except Exception as e:
			print(e)
			endereco = {}
		usuario = Usuario.objects.get(id=self.kwargs['usuario_id'])
		if usuario.tipo_usuario ==  'C':
			pessoa = Cliente.objects.get(usuario__id=self.kwargs['usuario_id'])
		else:
			pessoa = Empreendedor.objects.get(usuario__id=self.kwargs['usuario_id'])
		context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context = {
			#'usuario': Usuario.objects.get(id=self.kwargs['id']),
			#'cidades': Cidade.objects.all()
			'cidades': CITIES_CHOICES,
			'usuario': Usuario.objects.get(id=self.kwargs['usuario_id']),
			'endereco': endereco,
			'pessoa': pessoa,
			
		}
		return context

class empreendedores(ListView):
	model = Empreendedor
	template_name = 'services.html'

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
	
		context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context = {
			#'usuario': Usuario.objects.get(id=self.kwargs['id']),
			'id': self.kwargs['id'],
		'empreendedores' : Empreendedor.objects.select_related('usuario').prefetch_related(
			Prefetch('usuario__endereco_set', queryset=Endereco.objects.all(), to_attr='enderecos')),
		
			'usuario': Usuario.objects.get(id=self.kwargs['id']),
		}
		return context
class detail_empreendedor(DetailView):
	model = Empreendedor
	template_name = 'pag_detalhe.html'

	def get_context_data(self, **kwargs):
		""" 		try:
			endereco = Endereco.objects.get(usuario__id=self.kwargs['usuario_id']),
		except Exception as e:
			endereco = {} """
		empreendedor = Empreendedor.objects.get(id=self.kwargs['pk'])
		try:
			endereco = Endereco.objects.get(usuario__id=empreendedor.usuario.id)
		except Exception as e:
			endereco = {}
        # Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context = {
			'usuario': Usuario.objects.get(id=self.kwargs['usuario_id']),
			'endereco': endereco,
			'empreendedor': empreendedor,
		}
		return context


@csrf_exempt
def logar(request):

	print(f'tipo pessoa: {request.POST.get('tipo_pessoa')}')
	if request.POST.get('tipo_pessoa') == 'C':
		usuarios = Usuario.objects.filter(is_active=True, tipo_usuario='C').values('username', 'senha', 'id')
	else:
		usuarios = Usuario.objects.filter(is_active=True, tipo_usuario='E').values('username', 'senha', 'id')
	for user in usuarios:
		if request.POST.get('usuario') == user['username'] and request.POST.get('senha') == user['senha']:
			mensagem = f"Usuário logado com sucesso."
			status = "sucess"
			query = urlencode({'id': user['id'], 'usuario': user['username'], 'status': status})
			url = 'usuarios:servicos' + '?' + query
			return redirect('usuarios:empreendedores', user['id'])
		
	mensagem = f"Usuário ou Senha inválidos!"
	status = "error"
	query = urlencode({'status': status, 'mensagem': mensagem})
	url = reverse('usuarios:login') + '?' + query	
	return redirect(url)
		

def apresentation(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

""" class registro(CreateView):
	form_class = ProdutoForm
	pk_url_kwarg = 'id'
	success_message = 'Usuário criado!'
	template_name = 'registro.html'
	model = Usuario """
def registro(request):
	return render(request, 'registro.html', {'cidades':CITIES_CHOICES})

@csrf_exempt
def create_user(request):
	print(f'requests: {request.POST}')
	cidade = request.POST.get('cidade') 
	numero = request.POST.get('numero') 
	#dados = json.loads(request.body)
	latitude = request.POST.get('latitude')
	longitude = request.POST.get('longitude')
	bairro = request.POST.get('bairro') if request.POST.get('bairro') else ''
	logradouro = request.POST.get('logradouro') if request.POST.get('logradouro') else ''
	telefone = request.POST.get('telefone') if request.POST.get('telefone') else ''
	senha = request.POST.get('senha')
	usuario = request.POST.get('usuario')
	razao_social = request.POST.get('razao_social')
	nome_fantasia = request.POST.get('nome_fantasia')
	cnpj = request.POST.get('cnpj')
	insc_estadual = request.POST.get('insc_estadual') if request.POST.get('insc_estadual') != '' else None
	cpf = request.POST.get('cpf')
	data_nascimento = request.POST.get('data_nascimento')
	nome = request.POST.get('nome')
	descricao_servicos = request.POST.get('descricao_servicos')
	email = request.POST.get('email')
	foto = request.FILES.get('foto')
	username = Usuario.objects.filter(username=usuario).values('username').count()  if Usuario.objects.filter(username=usuario).values('username').count() > 0 else 0
	print(f'encontrou: {username}')
	if username != 0:
		mensagem = f"O usuário enviado já existe ou alguns dados estão inconsistentes!"
		status = "error"
		
		query = urlencode({'status': status, 'mensagem': mensagem})
		url = reverse('usuarios:registro') + '?' + query
		
		return redirect(url)
	else:
		
		if cnpj:
			try:
				user = Usuario.objects.create(nome=usuario, senha=senha, tipo_usuario='E', username=usuario, password=senha, is_active=True, email=email, foto=foto)
				endereco = Endereco.objects.create(logradouro=logradouro, bairro=bairro, numero=numero, cidade=cidade, usuario=user, longitude=longitude, latitude=latitude)
				empresa = Empreendedor.objects.create(razao_social=razao_social, email=email, nome_fantasia=nome_fantasia, cnpj=cnpj, inscricao_estadual=insc_estadual, usuario=user, tipo_pessoa='J', telefone=telefone, descricao_servicos=descricao_servicos)
				empresa.save()
				user.save()


				#return redirect(url)
			except Exception as e:
				print(e)
			mensagem = f"Usuário {user.nome} criado com sucesso!"
			status = "sucess"

			query = urlencode({'status': status, 'mensagem': mensagem})
			url = reverse('usuarios:registro') + '?' + query
		elif cpf:
			try:
				user = Usuario.objects.create(nome=usuario, senha=senha, tipo_usuario='C', username=usuario, password=senha, is_active=True, email=email, foto=foto)
				endereco = Endereco.objects.create(logradouro=logradouro, bairro=bairro, numero=numero, cidade=cidade, usuario=user)
				user.save()
				cliente = Cliente.objects.create(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, usuario=user, telefone=telefone)
				cliente.save()
			except Exception as e:
				print(e)
			mensagem = f"Usuário {user.nome} criado com sucesso!"
			status = "sucess"
			query = urlencode({'status': status, 'mensagem': mensagem})
			url = reverse('usuarios:registro') + '?' + query	

		return redirect(url)

		#object = User.objects.create(nome=usuario, senha=senha, tipo_usuario='C', username=usuario, password=senha, is_active=True)

def sobre(request):
	return render(request, 'sobre.html')