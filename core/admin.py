from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, EstadoCivil, Nacionalidade, Profissao, Genero,
    PessoaFisica, PessoaJuridica
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Perfil", {"fields": ("perfil",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Perfil", {"fields": ("perfil",)}),)
    list_display = ("username", "email", "first_name", "last_name", "perfil", "is_staff")

admin.site.register(EstadoCivil)
admin.site.register(Nacionalidade)
admin.site.register(Profissao)
admin.site.register(Genero)

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "data_nasc", "email", "telefone", "criado_em")
    search_fields = ("nome", "cpf", "email")
    list_filter = ("est_civil", "nacionalidade", "genero")

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "razao_social", "email", "telefone", "criado_em")
    search_fields = ("nome", "cnpj", "razao_social", "email")