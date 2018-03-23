from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UsuarioForm

# Create your views here.

def usuario_login(request):
    """Função para o formulário de entrada no sistema"""

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    return render(request, 'accounts/usuario_login.html')


def usuario_logout(request):
    """Função para a ação de saída do sistema"""

    logout(request)
    return redirect('accounts:usuario_login')


def usuario_registrar(request):
    """Função para o formulário de criação de usuários para o sistema"""

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            u = form.save()
            u.set_password(u.password)
            u.save()
            messages.success(request, 'Usuário registrado com sucesso! Utilize o formulário abaixo para fazer login.')
            return redirect('accounts:usuario_login')
    else:
        form = UsuarioForm()
    return render(request, 'accounts/usuario_registrar.html', {'form': form})


def alterar_senha(request):
    """Função para o formulário de troca de senha dos usuários do sistema"""

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('accounts:alterar_senha')
        else:
            messages.error(request, 'Não foi possível alterar a sua senha!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/alterar_senha.html', {'form': form})


# Tela inicial
@login_required
def home(request):
    """Função para a tela inicial do sistema"""

    return render(request, 'accounts/home.html', {'home': home})
