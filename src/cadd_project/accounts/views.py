from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, \
                    update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UsuarioForm
from sca.models import Users, Professor, Aluno
from cadd.models import Membro, Comissao, Convocacao, Reuniao, Perfil
from cadd.forms import PerfilForm
from cadd.utils import tipo_usuario, vida_academica, nome_sigla_curso, \
                    versao_curso

# Create your views here.

def usuario_registrar(request):
    """
    Função para o formulário de criação de usuários para o sistema
    """

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                # Pesquisa na tabela Users do SCA se o usuário é registrado
                usuario_login = Users.objects.using('sca').get(
                            login__iexact=request.POST.get('username')
                        )
                if 'Prof' in tipo_usuario(request.POST.get('username'), 0):
                    usuario = Professor.objects.using('sca').get(
                            matricula__iexact=usuario_login.matricula
                        )
                else:
                    usuario = Aluno.objects.using('sca').get(
                            matricula__iexact=usuario_login.matricula
                        )
                u = form.save(commit=False)
                u.set_password(u.password)
                u.username = usuario_login.nome
                u.email = usuario_login.email
                u.save()
                perfil = Perfil.objects.all()
                perfil.create(user=u.id, matricula=usuario_login.matricula,
                        idusuario=usuario.id)
                messages.success(request, 'Usuário registrado com sucesso! ' +
                        'Utilize o formulário abaixo para fazer login.')
                return redirect('accounts:usuario_login')
            except:
                messages.error(request, 'Usuário não cadastrado no sistema SCA!')
        else:
            if User.objects.filter(username=request.POST.get('username')):
                messages.error(request, 'Matrícula já registrada!')
            if (request.POST.get('password') != request.POST.get('new_password1')):
                messages.error(request, 'Senhas diferentes!')
            if len(request.POST.get('password')) < 8:
                messages.error(request, 'Senha não está com o comprimento mínimo de 8 caracteres!')

    else:
        form = UsuarioForm()

    return render(request, 'accounts/registro.html', {'form': form})

def usuario_login(request):
    """
    Função para o formulário de entrada no sistema
    """

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = Perfil.objects.get(matricula=username)


        user = authenticate(username=usuario.user.username, password=password)
        if user:
            if Users.objects.using('sca').get(login__iexact=username):
                login(request, user)
                tipo = tipo_usuario(usuario.matricula, 0)

            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Usuário não cadastrado ou senha inválida!')

    return render(request, 'accounts/login.html')

@login_required
def usuario_logout(request):
    """
    Função para a saída do sistema
    """

    logout(request)
    return redirect('accounts:usuario_login')

@login_required
def usuario_perfil(request):
    """
    Função para o formulário de troca de senha dos usuários do sistema
    """

    perfil = get_object_or_404(Perfil, user=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        form2 = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('accounts:usuario_perfil')
        else:
            if not form2.is_valid():
                messages.error(request, 'Não foi possível alterar a sua senha!')

        if form2.is_valid():
            outros = form2.save()
            messages.success(request, 'Parâmetro alterado com sucesso!')
            return redirect('accounts:usuario_perfil')
        else:
            if not form.is_valid():
                messages.error(request, 'Não foi possível alterar o parâmetro!')
    else:
        form = PasswordChangeForm(request.user)
        form2 = PerfilForm(instance=perfil)

    return render(request, 'accounts/perfil.html', {
                        'form': form,
                        'form2': form2,
                    })

# Tela inicial
@login_required
def home(request):
    """
    Função de saída para a tela inicial do sistema
    """

    membro = ""
    comissoes = ""
    convocacao = ""
    reunioes = ""
    matricula = ""
    nomecurso = ""
    versaocurso = ""
    criticidade = ""
    periodos = ""
    reprovadas = ""

    usuario = Perfil.objects.get(user=request.user.id)
    tipousuario = tipo_usuario(usuario.matricula,0)
    if 'Prof' in tipousuario:
        membro = Membro.objects.filter(professor=usuario.idusuario).values_list('comissao')
        comissoes = Comissao.objects.filter(id__in=membro)
        if not membro:
            messages.error(request, 'Professor(a), o Sr(a) não está cadastrado(a) em nenhuma comissão de apoio!')

    if 'Aluno' in tipousuario:
        convocacao = Convocacao.objects.filter(aluno=usuario.idusuario).values_list('reuniao')
        reunioes = Reuniao.objects.filter(id__in=convocacao)

        # processamento da vida acadêmica do aluno logado
        vidaacademica = vida_academica(usuario.idusuario)
        reprovadas = vidaacademica[3]
        # Verificação do nome do curso, versão, faixa de criticidade e periodos
#        matricula = request.user.username
        nomecurso = nome_sigla_curso(usuario.idusuario)[0]
        versaocurso = versao_curso(usuario.idusuario)
        criticidade = vidaacademica[4]
        periodos = vidaacademica[6]
        # Convocação para alguma reunião
        if not convocacao:
            messages.error(request, 'Aluno(a), você não possui nenhuma reunião agendada!')

    return render(request, 'accounts/home.html', {
                    'home': home,
                    'ativoInicio': True,
                    'membro': membro,
                    'comissoes': comissoes,
                    'reunioes': reunioes,
#                    'matricula': matricula,
                    'nomecurso': nomecurso,
                    'versaocurso':versaocurso,
                    'periodos': periodos,
                    'criticidade': criticidade,
                    'reprovadas': reprovadas
                })
