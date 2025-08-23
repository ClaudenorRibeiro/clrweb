from django import forms
from .models import PessoaFisica, PessoaJuridica

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = [
            "nome", "email", "telefone", "endereco",
            "data_nasc", "cpf", "est_civil", "nacionalidade",
            "rg_num", "rg_orgao", "pis", "profissao",
            "ctps_num", "ctps_serie", "pai", "mae",
            "cep", "logradouro", "num_end", "compl_end",
            "bairro", "cidade", "uf",
            "todos", "genero", "nomeSocial",
            "dataCad",
        ]


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = [
            "nome", "email", "telefone", "endereco",
            "razao_social", "cnpj",
            "cep", "logradouro", "num_end", "compl_end",
            "bairro", "cidade", "uf",
            "todos",
            "dataCad",
        ]