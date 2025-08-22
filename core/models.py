from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    PERFIS = [
        ('ADMIN', 'Administrador'),
        ('ADV', 'Advogado'),
        ('EST', 'Estagiário'),
        ('FIN', 'Financeiro'),
    ]
    perfil = models.CharField(max_length=20, choices=PERFIS, default='ADV')

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"


class Pessoa(models.Model):
    TIPOS = [
        ('FISICA', 'Pessoa Física'),
        ('JURIDICA', 'Pessoa Jurídica'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS)
    nome = models.CharField(max_length=200)
    documento = models.CharField(max_length=50, unique=True)  # CPF ou CNPJ
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
