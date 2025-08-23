from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, EstadoCivil, Nacionalidade, Profissao, Genero,
    PessoaFisica, PessoaJuridica
)
from .models import (
    Forum, Vara, StatusProc, TipoProc, NomeTituloProc,
    Processo, TituloProcAutor, TituloProcReu, Pasta
)

from .models import EmailPF, EmailPJ, TelefonePF, TelefonePJ

from .models import TipoPessoa, TipoPerfilPessoa, HistoricoUsuario


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


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("nomeForum", "cidade", "uf", "ultimaAlteracao")
    search_fields = ("nomeForum", "cidade", "uf")

@admin.register(Vara)
class VaraAdmin(admin.ModelAdmin):
    list_display = ("nomeVara", "idForum", "cidade", "uf", "ultimaAlteracao")
    search_fields = ("nomeVara", "cidade", "uf")
    list_filter = ("idForum",)

admin.site.register(StatusProc)
admin.site.register(TipoProc)
admin.site.register(NomeTituloProc)

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ("numProc", "idTblTipoProc", "idStatusProc", "idTblForum", "idTblVara", "valorCausa", "dataDistribuicao")
    search_fields = ("numProc",)
    list_filter = ("idTblTipoProc", "idStatusProc", "idTblForum", "idTblVara")

@admin.register(TituloProcAutor)
class TituloProcAutorAdmin(admin.ModelAdmin):
    list_display = ("NomeTituloProc", "idTblProc", "autor", "numPasta", "dataCad")
    search_fields = ("NomeTituloProc", "autor")

@admin.register(TituloProcReu)
class TituloProcReuAdmin(admin.ModelAdmin):
    list_display = ("NomeTituloProc", "idTblProc", "reu", "numPasta", "dataCad")
    search_fields = ("NomeTituloProc", "reu")

@admin.register(Pasta)
class PastaAdmin(admin.ModelAdmin):
    list_display = ("numPasta", "idTblProc")
    search_fields = ("numPasta",)


@admin.register(EmailPF)
class EmailPFAdmin(admin.ModelAdmin):
    list_display = ("emailPF", "idTblPF", "dataCad", "obs")
    search_fields = ("emailPF", "obs")
    list_filter = ("dataCad",)

@admin.register(EmailPJ)
class EmailPJAdmin(admin.ModelAdmin):
    list_display = ("emailPJ", "idTblPJ", "dataCad", "obs")
    search_fields = ("emailPJ", "obs")
    list_filter = ("dataCad",)

@admin.register(TelefonePF)
class TelefonePFAdmin(admin.ModelAdmin):
    list_display = ("numTelefone", "idTblPF", "dataCad", "obs")
    search_fields = ("numTelefone", "obs")
    list_filter = ("dataCad",)

@admin.register(TelefonePJ)
class TelefonePJAdmin(admin.ModelAdmin):
    list_display = ("numTelefone", "idTblPJ", "dataCad", "obs")
    search_fields = ("numTelefone", "obs")
    list_filter = ("dataCad",)


@admin.register(TipoPessoa)
class TipoPessoaAdmin(admin.ModelAdmin):
    list_display = ("tipoPessoa", "dataCad")
    search_fields = ("tipoPessoa",)
    list_filter = ("dataCad",)

@admin.register(TipoPerfilPessoa)
class TipoPerfilPessoaAdmin(admin.ModelAdmin):
    list_display = ("TipoPerfilPessoa", "dataCad")
    search_fields = ("TipoPerfilPessoa",)
    list_filter = ("dataCad",)

@admin.register(HistoricoUsuario)
class HistoricoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("idUsuario", "data", "historico")
    search_fields = ("idUsuario__username",)
    list_filter = ("data",)