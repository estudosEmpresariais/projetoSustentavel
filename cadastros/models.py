from django.db import models
from usuarios.models import Usuario
#from .city import UF_CHOICES
# Create your models here.
""" class Cidade(models.Model):
   nome = models.CharField('Cidade', max_length=80)
   uf = models.CharField('UF', max_length=2) """

class Pessoa(models.Model):
   TIPO_PESSOA = (
      ('F', 'Física'),
      ('J', 'Jurídica'),
   )
   email = models.CharField('Email', max_length=40, null=True, blank=True)
   telefone = models.CharField('Telefone', null=True, blank=True)
   tipo_pessoa = models.CharField('Tipo Pessoa', max_length=1, default='F', choices=TIPO_PESSOA)
   usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)

"""    def getTelefone(self):
      formated_string = f"(%d%d)" % int(self.telefone) if self.telefone else ''
      return formated_string """

class Cliente(Pessoa):
   nome = models.CharField('Nome', max_length=50)
   cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
   data_nascimento = models.DateTimeField()

class Empreendedor(Pessoa):
   razao_social = models.CharField('Nome', max_length=60)
   nome_fantasia = models.CharField('Nome', max_length=60)
   cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
   inscricao_estadual = models.CharField('Inscrição Estadual', max_length=9, null=True, blank=True)
   descricao_servicos = models.CharField('Descrição Serviços', max_length=100, null=True, blank=True)
   

class Endereco(models.Model):
   logradouro = models.CharField('Logradouro', max_length=100, null=True, blank=True)
   bairro = models.CharField('Bairro', max_length=50, null=True, blank=True)
   complemento = models.CharField('Bairro', max_length=50, null=True, blank=True)
   latitude = models.CharField('Latitude', null=True, blank=True)
   longitude = models.CharField('Longitude', null=True, blank=True)
   numero = models.IntegerField('Número', null=True, blank=True)
   #uf = models.CharField("Estado", max_length=2, choices=UF_CHOICES,null=True)
   cidade = models.CharField("Cidade", max_length=50, null=True)
   usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
