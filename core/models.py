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


class Forum(models.Model):
    abrevNomeForum = models.CharField(max_length=50, blank=True, null=True)
    nomeForum = models.CharField(max_length=50, blank=True, null=True)

    cep = models.CharField(max_length=8, blank=True, null=True)
    logradouro = models.CharField(max_length=300, blank=True, null=True)
    num_end = models.CharField(max_length=11, blank=True, null=True)
    compl_end = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    dataCad = models.DateField(blank=True, null=True)
    ultimaAlteracao = models.DateTimeField(auto_now=True)
    idUserQueCadastrou = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="foruns_cadastrados"
    )
    idUserQueAlterou = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="foruns_alterados"
    )

    def __str__(self):
        return self.nomeForum or f"Fórum {self.id}"


class Vara(models.Model):
    idForum = models.ForeignKey(Forum, on_delete=models.RESTRICT, blank=True, null=True)
    abrevNomeVara = models.CharField(max_length=50, blank=True, null=True)
    numVara = models.CharField(max_length=3, blank=True, null=True)
    nomeVara = models.CharField(max_length=50, blank=True, null=True)

    cep = models.CharField(max_length=8, blank=True, null=True)
    logradouro = models.CharField(max_length=300, blank=True, null=True)
    num_end = models.CharField(max_length=11, blank=True, null=True)
    compl_end = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    dataCad = models.DateField(blank=True, null=True)
    ultimaAlteracao = models.DateTimeField(auto_now=True)
    idUserQueCadastrou = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="varas_cadastradas"
    )
    idUserQueAlterou = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="varas_alteradas"
    )
    telVara = models.CharField(max_length=50, blank=True, null=True)
    emailVara = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nomeVara or f"Vara {self.id}"


class StatusProc(models.Model):
    statusProc = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.statusProc or f"Status {self.id}"


class TipoProc(models.Model):
    tipoProc = models.CharField(max_length=50, blank=True, null=True)
    dataCad = models.DateField(blank=True, null=True)
    dataAlteracao = models.DateField(blank=True, null=True)
    idAlteradoPorUsuario = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="tipoproc_alterados"
    )

    def __str__(self):
        return self.tipoProc or f"Tipo {self.id}"


class NomeTituloProc(models.Model):
    # Seu SQL tinha 'nomeDoTitulo' como INT(11); vou tratar como texto (mais natural para "nome").
    nomeDoTitulo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nomeDoTitulo or f"Nome do Título {self.id}"


# ======================
# PROCESSO PRINCIPAL (tblProc)
# ======================
class Processo(models.Model):
    numProc = models.CharField(max_length=45, blank=True, null=True, db_index=True)
    idTblTipoProc = models.ForeignKey(TipoProc, on_delete=models.RESTRICT, blank=True, null=True)
    idStatusProc = models.ForeignKey(StatusProc, on_delete=models.RESTRICT, blank=True, null=True)
    idTblForum = models.ForeignKey(Forum, on_delete=models.RESTRICT, blank=True, null=True)
    idTblVara = models.ForeignKey(Vara, on_delete=models.RESTRICT, blank=True, null=True)

    valorCausa = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    dataDistribuicao = models.DateField(blank=True, null=True)

    dataCad = models.DateTimeField(auto_now_add=True)
    dataAlteracao = models.DateField(blank=True, null=True)

    idAlteradoPorUsuario = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="processos_alterados"
    )
    InstanciaProc = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.numProc or f"Processo {self.id}"


# ======================
# TÍTULOS (Autor/Réu) e PASTA
# ======================
class TituloProcAutor(models.Model):
    NomeTituloProc = models.CharField(max_length=200, blank=True, null=True)
    idTblProc = models.ForeignKey(Processo, on_delete=models.RESTRICT, blank=True, null=True)
    autor = models.CharField(max_length=45, blank=True, null=True)
    dataAlteracao = models.DateField(blank=True, null=True)
    dataCad = models.DateField(blank=True, null=True)
    idAlteradoPorUsuario = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="titulos_autor_alterados"
    )
    numPasta = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.NomeTituloProc or f"Título Autor {self.id}"


class TituloProcReu(models.Model):
    NomeTituloProc = models.CharField(max_length=200, blank=True, null=True)
    idTblProc = models.ForeignKey(Processo, on_delete=models.RESTRICT, blank=True, null=True)
    reu = models.CharField(max_length=50, blank=True, null=True)
    dataAlteracao = models.DateField(blank=True, null=True)
    dataCad = models.DateField(blank=True, null=True)
    idAlteradoPorUsuario = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="titulos_reu_alterados"
    )
    numPasta = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.NomeTituloProc or f"Título Réu {self.id}"


class Pasta(models.Model):
    numPasta = models.IntegerField(blank=True, null=True)
    idTblProc = models.ForeignKey(Processo, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return f"Pasta {self.numPasta or self.id}"
    

class EmailPF(models.Model):
    emailPF = models.CharField(max_length=100, default="", blank=False)
    obs = models.CharField(max_length=150, default="", blank=False)
    idTblPF = models.ForeignKey(PessoaFisica, on_delete=models.RESTRICT, blank=True, null=True, related_name="emails_pf")
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.emailPF or f"EmailPF {self.id}"


class TelefonePF(models.Model):
    idTblPF = models.ForeignKey(PessoaFisica, on_delete=models.RESTRICT, blank=True, null=True, related_name="telefones_pf")
    numTelefone = models.CharField(max_length=20, default="", blank=False)
    obs = models.CharField(max_length=50, default="", blank=False)
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.numTelefone or f"TelefonePF {self.id}"


# ======================
# Contatos de Pessoa Jurídica
# ======================
class EmailPJ(models.Model):
    emailPJ = models.CharField(max_length=50, default="", blank=False)
    obs = models.CharField(max_length=100, default="", blank=False)
    idTblPJ = models.ForeignKey(PessoaJuridica, on_delete=models.RESTRICT, blank=True, null=True, related_name="emails_pj")
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.emailPJ or f"EmailPJ {self.id}"


class TelefonePJ(models.Model):
    idTblPJ = models.ForeignKey(PessoaJuridica, on_delete=models.RESTRICT, blank=True, null=True, related_name="telefones_pj")
    numTelefone = models.CharField(max_length=20, default="", blank=False)
    obs = models.CharField(max_length=50, default="", blank=False)
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.numTelefone or f"TelefonePJ {self.id}"
    

class TipoPessoa(models.Model):
    tipoPessoa = models.CharField(max_length=50, blank=True, null=True)
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.tipoPessoa or f"TipoPessoa {self.id}"


class TipoPerfilPessoa(models.Model):
    # No SQL: NOT NULL DEFAULT '0' → aqui mantemos obrigatório (sem null), com default "0"
    TipoPerfilPessoa = models.CharField(max_length=50, default="0")
    dataCad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.TipoPerfilPessoa


# ======================
# Histórico de ações do usuário
# ======================
class HistoricoUsuario(models.Model):
    idUsuario = models.ForeignKey(
        "Usuario", on_delete=models.RESTRICT, blank=True, null=True, related_name="historicos"
    )
    # No SQL: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    data = models.DateTimeField(auto_now_add=True)
    # No SQL: historico INT(11); parece um código/enum.
    # Mantemos como IntegerField (podemos evoluir para TextField caso você queira texto livre).
    historico = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Histórico {self.id} - Usuário {self.idUsuario_id or '-'}"