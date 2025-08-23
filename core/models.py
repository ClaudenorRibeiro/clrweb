from django.db import models
from django.contrib.auth.models import AbstractUser


# ======================
# Usuário com perfil
# ======================
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


# ======================
# Tabelas de referência (simples)
# ======================
class EstadoCivil(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Nacionalidade(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Profissao(models.Model):
    descricao = models.CharField(max_length=120)

    def __str__(self):
        return self.descricao


class Genero(models.Model):
    descricao = models.CharField(max_length=60)

    def __str__(self):
        return self.descricao


# ======================
# Classe base comum
# ======================
class PessoaBase(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


# ======================
# Pessoa Física (com campos do seu SQL)
# ======================
class PessoaFisica(PessoaBase):
    data_nasc = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True, db_index=True)  # sem pontuação
    est_civil = models.ForeignKey(EstadoCivil, on_delete=models.RESTRICT, blank=True, null=True)
    nacionalidade = models.ForeignKey(Nacionalidade, on_delete=models.RESTRICT, blank=True, null=True)
    rg_num = models.CharField(max_length=50, blank=True, null=True)
    rg_orgao = models.CharField(max_length=10, blank=True, null=True)
    pis = models.CharField(max_length=50, blank=True, null=True)
    profissao = models.ForeignKey(Profissao, on_delete=models.RESTRICT, blank=True, null=True)
    ctps_num = models.CharField(max_length=50, blank=True, null=True)
    ctps_serie = models.CharField(max_length=50, blank=True, null=True)
    pai = models.CharField(max_length=200, blank=True, null=True)
    mae = models.CharField(max_length=200, blank=True, null=True)

    # Endereço detalhado
    cep = models.CharField(max_length=8, blank=True, null=True)
    logradouro = models.CharField(max_length=300, blank=True, null=True)
    num_end = models.CharField(max_length=11, blank=True, null=True)
    compl_end = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    todos = models.CharField(max_length=500, blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT, blank=True, null=True)
    nomeSocial = models.CharField(max_length=50, blank=True, null=True)

    dataCad = models.DateField(blank=True, null=True)
    ultimaAlteracao = models.DateTimeField(auto_now=True)  # espelha o comportamento do SQL
    tipoPessoa = models.CharField(max_length=2, default='F')

    idUserQueCadastrou = models.ForeignKey(
        Usuario, on_delete=models.RESTRICT, blank=True, null=True, related_name='pf_cadastradas'
    )
    idUserQueAlterou = models.ForeignKey(
        Usuario, on_delete=models.RESTRICT, blank=True, null=True, related_name='pf_alteradas'
    )


# ======================
# Pessoa Jurídica (com campos do seu SQL)
# ======================
class PessoaJuridica(PessoaBase):
    razao_social = models.CharField(max_length=200, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True, db_index=True)  # com máscara futura

    # Endereço detalhado (no SQL a maioria é NOT NULL; aqui deixamos flexível no desenvolvimento)
    cep = models.CharField(max_length=8, blank=True, null=True)
    logradouro = models.CharField(max_length=150, blank=True, null=True)
    num_end = models.CharField(max_length=11, blank=True, null=True)
    compl_end = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    todos = models.CharField(max_length=400, blank=True, null=True)

    ultima_alteracao = models.DateTimeField(auto_now=True)  # default CURRENT_TIMESTAMP no SQL
    dataCad = models.DateField(blank=True, null=True)
    tipoPessoa = models.CharField(max_length=2, default='J')

    idUserQueCadJud = models.ForeignKey(
        Usuario, on_delete=models.RESTRICT, blank=True, null=True, related_name='pj_cadastradas'
    )
