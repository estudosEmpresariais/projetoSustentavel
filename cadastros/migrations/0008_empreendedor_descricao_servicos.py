# Generated by Django 5.2 on 2025-05-06 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_alter_pessoa_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='empreendedor',
            name='descricao_servicos',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descrição Serviços'),
        ),
    ]
