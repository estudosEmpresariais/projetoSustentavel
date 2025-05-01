from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Usuario(User):
   TIPO_USUARIO = (
      ('C', 'Cliente'),
      ('E', 'Empreendedor'),
   )
   # ID	username	nome	email	senha	tipo_usuario(cliente ou empreendedor)
   nome = models.CharField('Nome', max_length=50 )
   senha = models.CharField('Senha', max_length=8 )
   tipo_usuario = models.CharField('Tipo Usuário', max_length=1, choices=TIPO_USUARIO, default='C')

'''
PESSOA									
ID	cpf/cnpj								
									
EMPRESA									
ID	razão social	cnpj	telefone	categoria	nome fantasia	inscricao estadual	usuario_id		
									
ENDERECO									
ID	Logradouro	bairro	numero	cidade_id	ponto referencia	latitude	logitude	complemento	empresa_id
									
CLIENTE									
ID	nome	email	cpf	data_nascimento					

'''


