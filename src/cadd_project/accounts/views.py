from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UsuarioForm
from sca.models import Users, Useruserprofile, UserProfile

#from MySQLdb import IntegrityError
#from django.db import transaction
from django.contrib.auth.models import User

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
            if Users.objects.using('sca').get(login__iexact=username):
                login(request, user)
#            else:
#                messages.error(request, 'Usuário não cadastrado no sistema SCA!')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Usuário não cadastrado ou senha inválida!')
    return render(request, 'accounts/usuario_login.html')


@login_required
def usuario_logout(request):
    """Função para a saída do sistema"""

    logout(request)
    return redirect('accounts:usuario_login')

def usuario_registrar(request):
    """Função para o formulário de criação de usuários para o sistema"""

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
#            try:
            # Pesquisa na tabela de usuários do SCA o usuário a ser registrado
            usuario = Users.objects.using('sca').get(login__iexact=request.POST.get('username'))
            # Caso seja realizado um get na tabela N:N o resultado já sai para a tabela apropriada
            # Nesse caso, necessitou saber quais são as ids das roles do SCA
            idAlunoProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_ALUNO')
            idProfProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_PROFESSOR')
            idAdminProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_SECAD')
            tipoUsuario = ''
            # Caso seu perfil no SCA seja de role SECAD
            if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idAdminProfile).exists():
                tipoUsuario = 'Administrador'
            # Caso seu perfil no SCA seja de role Professor
            if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idProfProfile).exists():
                if tipoUsuario != '':
                    tipoUsuario += '/Professor'
                else:
                    tipoUsuario = 'Professor'
            # Caso seu perfil no SCA seja de role Aluno
            if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idAlunoProfile).exists():
                tipoUsuario = 'Aluno'
            u = form.save()
            u.set_password(u.password)
            u.first_name = tipoUsuario
            u.last_name = usuario.nome
            u.email = usuario.email
            u.save()
            messages.success(request, 'Usuário registrado com sucesso! Utilize o formulário abaixo para fazer login.')
            return redirect('accounts:usuario_login')
#            except IntegrityError:
#                messages.error(request, "Matrícula já cadastrada!")
#                form.rollback()

        else:
            if User.objects.filter(username=request.POST.get('username')):
                messages.error(request, 'Matrícula já registrada!')
            if (request.POST.get('password') != request.POST.get('new_password1')):
                messages.error(request, 'Senhas diferentes!')
    else:
        form = UsuarioForm()
    return render(request, 'accounts/usuario_registrar.html', {'form': form})


@login_required
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
    """Função de saída para a tela inicial do sistema"""

    return render(request, 'accounts/home.html', {'home': home})
