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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from itertools import groupby
from urllib.parse import urlencode
from .models import Usuario
from cadastros.models import Pessoa, Cliente, Empreendedor, Endereco
from django.urls import reverse
from django.db.models.aggregates import Avg, Sum, Count, Min, Max
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class empreendedores(ListView):
	model = Usuario
	template_name = 'services.html'

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		print(f'variavel id: {self.kwargs['id']}')
		context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context = {
			#'usuario': Usuario.objects.get(id=self.kwargs['id']),
			'id': self.kwargs['id'],
		}
		return context
class detail_empreendedor(DetailView):
	model = Usuario
	template_name = 'pag_detalhe.html'

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context = {
			'usuario': Usuario.objects.get(id=self.kwargs['pk']),
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
	return render(request, 'registro.html')

@csrf_exempt
def create_user(request):
	senha = request.POST.get('senha')
	usuario = request.POST.get('usuario')
	razao_social = request.POST.get('razao_social')
	nome_fantasia = request.POST.get('nome_fantasia')
	cnpj = request.POST.get('cnpj')
	insc_estadual = request.POST.get('insc_estadual') if request.POST.get('insc_estadual') != '' else None
	cpf = request.POST.get('cpf')
	data_nascimento = request.POST.get('data_nascimento')
	nome = request.POST.get('nome')
	email = request.POST.get('email')
	foto = request.FILES.get('foto')
	username = Usuario.objects.filter(username=usuario).values('username').count()  if Usuario.objects.filter(username=usuario).values('username').count() > 0 else 0
	if username != 0:
		mensagem = f"O usuário enviado já existe ou alguns dados estão inconsistentes!"
		status = "error"
		
		query = urlencode({'status': status, 'mensagem': mensagem})
		url = reverse('usuarios:registro') + '?' + query
		
		return redirect(url)
	else:
		if cnpj:
			user = Usuario.objects.create(nome=usuario, senha=senha, tipo_usuario='E', username=usuario, password=senha, is_active=True, email=email, foto=foto)
			
			user.save()
			empresa = Empreendedor.objects.create(razao_social=razao_social, nome_fantasia=nome_fantasia, cnpj=cnpj, inscricao_estadual=insc_estadual, usuario=user, tipo_pessoa='J')
			empresa.save()
			mensagem = f"Usuário {user.nome} criado com sucesso!"
			status = "sucess"
			
			query = urlencode({'status': status, 'mensagem': mensagem})
			url = reverse('usuarios:registro') + '?' + query
			return redirect(url)
		elif cpf:
			user = Usuario.objects.create(nome=usuario, senha=senha, tipo_usuario='C', username=usuario, password=senha, is_active=True, email=email, foto=foto)
			user.save()
			cliente = Cliente.objects.create(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, usuario=user)
			cliente.save()
			mensagem = f"Usuário {user.nome} criado com sucesso!"
			status = "sucess"
			query = urlencode({'status': status, 'mensagem': mensagem})
			url = reverse('usuarios:registro') + '?' + query	
			return redirect(url)

		#object = User.objects.create(nome=usuario, senha=senha, tipo_usuario='C', username=usuario, password=senha, is_active=True)

def sobre(request):
	return render(request, 'sobre.html')