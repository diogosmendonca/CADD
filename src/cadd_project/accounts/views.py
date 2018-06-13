from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.core.cache import cache     # para uso do cached table

from .forms import UsuarioForm
from sca.models import Users, Professor, Aluno
from cadd.models import Membro, Comissao, Convocacao, Reuniao
from cadd.utils import tipo_usuario

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
                tipo = tipo_usuario(user.username, 0)

            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Usuário não cadastrado ou senha inválida!')
    return render(request, 'accounts/login.html')


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
            try:
                # Pesquisa na tabela de usuários do SCA se o usuário é registrado
                usuario_login = Users.objects.using('sca').get(login__iexact=request.POST.get('username'))
                if 'Prof' in tipo_usuario(request.POST.get('username'), 0):
                    usuario = Professor.objects.using('sca').get(matricula__iexact=usuario_login.matricula)
                else:
                    usuario = Aluno.objects.using('sca').get(matricula__iexact=usuario_login.matricula)
                u = form.save(commit=False)
                u.set_password(u.password)
                u.first_name = usuario.id
                u.last_name = usuario_login.nome
                u.email = usuario_login.email
                u.save()
                messages.success(request, 'Usuário registrado com sucesso! Utilize o formulário abaixo para fazer login.')
                return redirect('accounts:usuario_login')
            except:
                messages.error(request, 'Usuário não cadastrado no sistema SCA!')
        else:
            if User.objects.filter(username=request.POST.get('username')):
                messages.error(request, 'Matrícula já registrada!')
            if (request.POST.get('password') != request.POST.get('new_password1')):
                messages.error(request, 'Senhas diferentes!')
    else:
        form = UsuarioForm()
    return render(request, 'accounts/registrar.html', {'form': form})


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

    membro = ""
    comissoes = ""
    convocacao = ""
    reunioes = ""
    if 'Prof' in tipo_usuario(request.user.username, 0):
        membro = Membro.objects.filter(professor=request.user.first_name).values_list('comissao')
        comissoes = Comissao.objects.filter(id__in=membro)
        if not membro:
            messages.error(request, 'Professor(a), o Sr(a) não está cadastrado(a) em nenhuma comissão de apoio!')

    if 'Aluno' in tipo_usuario(request.user.username, 0):
        convocacao = Convocacao.objects.filter(aluno=request.user.first_name).values_list('reuniao')
        reunioes = Reuniao.objects.filter(id__in=convocacao)
        if not convocacao:
            messages.error(request, 'Aluno(a), você não possui nenhuma reunião agendada!')

    return render(request, 'accounts/home.html', {
                    'home': home,
                    'ativoInicio': True,
                    'membro': membro,
                    'comissoes': comissoes,
                    'reunioes': reunioes
                })
