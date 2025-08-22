from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pessoa
from .forms import PessoaForm
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def _usuario_pode_gerir_pessoas(user):
    # Regra inicial: apenas ADMIN e ADV podem criar (depois refinamos)
    return getattr(user, "perfil", None) in ("ADMIN", "ADV")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def pessoas_list(request):
    pessoas = Pessoa.objects.all().order_by("-criado_em")
    return render(request, "pessoas_list.html", {"pessoas": pessoas})


@login_required
def pessoas_create(request):
    if not _usuario_pode_gerir_pessoas(request.user):
        return HttpResponseForbidden("Você não tem permissão para criar pessoas.")

    if request.method == "POST":
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona para a lista após criar
            from django.urls import reverse
            return redirect(reverse("pessoas_list"))
    else:
        form = PessoaForm()

    return render(request, "pessoas_form.html", {"form": form, "titulo": "Nova Pessoa"})


@login_required
def pessoas_edit(request, pessoa_id):
    if not _usuario_pode_gerir_pessoas(request.user):
        return HttpResponseForbidden("Você não tem permissão para editar pessoas.")

    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    if request.method == "POST":
        form = PessoaForm(request.POST, instance=pessoa)
        if form.is_valid():
            form.save()
            messages.success(request, "Pessoa atualizada com sucesso.")
            from django.urls import reverse
            return redirect(reverse("pessoas_list"))
    else:
        form = PessoaForm(instance=pessoa)

    return render(request, "pessoas_form.html", {"form": form, "titulo": "Editar Pessoa"})


@login_required
def pessoas_delete(request, pessoa_id):
    if not _usuario_pode_gerir_pessoas(request.user):
        return HttpResponseForbidden("Você não tem permissão para excluir pessoas.")

    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    if request.method == "POST":
        nome = pessoa.nome
        pessoa.delete()
        messages.success(request, f"Pessoa '{nome}' excluída.")
        from django.urls import reverse
        return redirect(reverse("pessoas_list"))

    return render(request, "pessoas_confirm_delete.html", {"pessoa": pessoa})


