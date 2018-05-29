from .models import Parametros
from sca.models import Users, UserProfile, Useruserprofile

def linhas_por_pagina():
    """Função que retorna a quantidade de itens por página cadastrada em parâmetros"""

    linhas = 5
    registros = Parametros.objects.filter(id=1).count()
    if registros != 0:
        linhas = Parametros.objects.get(pk=1).defaultitensporpagina
    return linhas

def tipo_usuario(username, registro):
    """Função que retorna o tipo de usuário vinculado ao SCA por meio do usuário logado"""

    # Pesquisa na tabela de usuários do SCA o usuário a ser registrado
    usuario = Users.objects.using('sca').get(login__iexact=username)
    # Caso seja realizado um get na tabela N:N o resultado já sai para a tabela apropriada
    # Nesse caso, necessitou saber quais são as ids das roles do SCA
    idProfProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_PROFESSOR')
    idAlunoProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_ALUNO')
    idAdminProfile = UserProfile.objects.using('sca').get(type__iexact='ROLE_SECAD')
    # Caso seu perfil no SCA seja de role SECAD e não seja para registro...
    if registro == 0:
        if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idAdminProfile).exists():
            return 'Admin'
    # Caso seu perfil no SCA seja de role Professor
    if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idProfProfile).exists():
        return 'Prof'
    # Caso seu perfil no SCA seja de role Aluno
    if Useruserprofile.objects.using('sca').filter(user=usuario, userprofile=idAlunoProfile).exists():
        return 'Aluno'
    return ''

def lista_comissoes():
    """Função que retorna o tipo de usuário vinculado ao SCA por meio do usuário logado"""

    return None
