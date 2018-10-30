from datetime import datetime
import os

from django.core.checks import messages
from django.http import request

from .models import Parametros, Perfil
from sca.models import Users, UserProfile, Useruserprofile, Aluno, Curso, \
    Itemhistoricoescolar, Disciplinasoriginais, \
    Blocoequivalencia, Disciplinasequivalentes, Versaocurso

PARAMS_ID = 1
ROLE_PROFESSOR = 'ROLE_PROFESSOR'
ROLE_ALUNO = 'ROLE_ALUNO'
ROLE_SECAD = 'ROLE_SECAD'


# Funções úteis
# Função para se saber o tipo do usuário logado
def tipo_usuario(matricula, registro):
    """
    Função que retorna o tipo de usuário por meio da ROLE do SCA e
    usuário logado
    """

    # Pesquisa na tabela de usuários do SCA o usuário a ser registrado
    usuario = Users.objects.using('sca').get(login__iexact=matricula)
    # Caso seja realizado um get na tabela N:N o resultado já sai para a tabela
    # apropriada. Nesse caso, necessitou saber quais são as ids das roles do SCA
    idProfProfile = UserProfile.objects.using('sca').get(
        type__iexact=ROLE_PROFESSOR
    )
    idAlunoProfile = UserProfile.objects.using('sca').get(
        type__iexact=ROLE_ALUNO
    )
    idAdminProfile = UserProfile.objects.using('sca').get(
        type__iexact=ROLE_SECAD
    )
    # Caso seu perfil no SCA seja de role SECAD e não seja para registro...
    if registro == 0:
        if Useruserprofile.objects.using('sca').filter(
                user=usuario, userprofile=idAdminProfile
        ).exists():
            return 'Admin'
    # Caso seu perfil no SCA seja de role Professor
    if Useruserprofile.objects.using('sca').filter(
            user=usuario, userprofile=idProfProfile
    ).exists():
        return 'Prof'
    # Caso seu perfil no SCA seja de role Aluno
    if Useruserprofile.objects.using('sca').filter(
            user=usuario, userprofile=idAlunoProfile
    ).exists():
        return 'Aluno'

    return ''


# Funções para valores de parâmetros
def reprovacoes_faixa_laranja_cursos_8_periodos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de 8 períodos ou mais para que esteja na
    faixa de criticidade laranja
    """

    reprovacoes = 2
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        reprovacoes = registros.reprovacurso8periodoslaranja

    return reprovacoes


def reprovacoes_faixa_vermelha_cursos_8_periodos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de 8 períodos ou mais para que esteja na
    faixa de criticidade vermelha
    """

    reprovacoes = 3
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        reprovacoes = registros.reprovacurso8periodosvermelha

    return reprovacoes


def reprovacoes_faixa_laranja_demais_cursos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de menos de 8 períodos para que esteja na
    faixa de criticidade laranja
    """

    reprovacoes = 1
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        reprovacoes = registros.reprovademaiscursoslaranja

    return reprovacoes


def reprovacoes_faixa_vermelha_demais_cursos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de menos de 8 períodos para que esteja na
    faixa de criticidade vermelha
    """

    reprovacoes = 2
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        reprovacoes = registros.reprovademaiscursosvermelha

    return reprovacoes


def formula_inicial_faixa_laranja():
    """
    Função que retorna a fórmula do valor inicial para cálculo das
    integralizações dos cursos para que esteja na faixa de
    criticidade laranja
    """

    formula = '2 * N'
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        formula = registros.qtdperiodosiniciallaranja

    return formula


def formula_final_faixa_laranja():
    """
    Função que retorna a fórmula do valor final para cálculo das
    integralizações dos cursos para que esteja na faixa de
    criticidade laranja
    """

    formula = '2 * N'
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        formula = registros.qtdperiodosfinallaranja

    return formula


def formula_faixa_vermelha():
    """
    Função que retorna a fórmula para cálculo das integralizações dos
    cursos para que esteja na faixa de criticidade vermelha
    """

    formula = '4 * N - 3'
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        formula = registros.qtdperiodosvermelha

    return formula


def min_creditos_preta():
    """
    Função que retorna a quantidade mínima de créditos por semana para um
    aluno que esteja na faixa de criticidade preta
    """

    creditos = 20
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        creditos = registros.mincreditosporperiodopreta

    return creditos


def max_creditos():
    """
    Função que retorna a quantidade máxima de créditos por semana para
    qualquer aluno
    """

    creditos = 28
    registros = Parametros.objects.get(pk=PARAMS_ID)
    if registros != 0:
        creditos = registros.maxcreditosporperiodo

    return creditos


def linhas_por_pagina(id_usuario):
    """
    Função que retorna a quantidade de linhas por página cadastrada na
    tabela perfil do usuário
    """

    linhas = 5
    registros = Perfil.objects.get(idusuario=id_usuario)
    if registros != 0:
        linhas = registros.itenspagina

    return linhas


# Funções gerais
def periodo_atual():
    """
    Função que retorna o ano e período atual
    """
    agora = datetime.now()
    ano = agora.year
    mes = agora.month
    # Mês de início das aulas do semestre
    if mes in [1, 2, 3, 4, 5, 6, 7]:
        periodo = 1
    else:
        periodo = 2
    retorno = ano, periodo, str(ano) + "." + str(periodo)

    return retorno


def proximo_periodo(periodos):
    """
    Função que retorna o ano e periodo conforme a quantidade de semestres
    selecionados
    """

    temp = periodo_atual()
    ano = temp[0]
    tperiodos = temp[1] + periodos
    if tperiodos % 2 == 0:
        periodo = 2
        ano = ano + (tperiodos // 2) - 1
    else:
        periodo = 1
        ano = ano + (tperiodos // 2)
    retorno = ano, periodo, str(ano) + "." + str(periodo)

    return retorno


def versao_curso(id_aluno):
    """
    Função que retorna a versão do curso do aluno e as cargas horária
    de disciplinas optativas e atividades complementares dessa versão
    """

    aluno = Aluno.objects.using('sca').get(id=id_aluno)
    versaocurso = aluno.versaocurso.numero
    cargahorariaoptativas = aluno.versaocurso.cargahorariaoptativas
    cargahorariaativcomp = aluno.versaocurso.cargahorariaativcomp
    retorno = versaocurso, cargahorariaoptativas, cargahorariaativcomp

    return retorno


def nome_sigla_curso(id_aluno):
    """
    Função que retorna o nome do curso do aluno logado
    """

    aluno = Aluno.objects.using('sca').get(id=id_aluno)
    t_curso = Curso.objects.using('sca').get(id=aluno.versaocurso.curso.id)
    nomecurso = t_curso.nome + " (" + t_curso.sigla + ")"
    retorno = nomecurso, t_curso.sigla, t_curso.id

    return retorno


def excluir_arquivo(documento):
    """
    Função que exclui o documento cadastrado e enviado para a pasta de
    mídias de documentos do projeto
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    try:
        os.remove('{}/{}'.format(MEDIA_ROOT, documento))
    except:
        messages.error(request, 'o arquivo não existe!')

    return None


# Função
def vida_academica(id_aluno):
    """
    Função que retorna a quantidade máxima de reprovações em uma disciplina
    para cálculo da faixa de criticidade do aluno logado

    TODO: Falta filtrar o item por ano e periodo nos itens de historico
    """

    # Recupera e armazena o aluno correspondente ao identificador passado no parâmetro
    aluno = Aluno.objects.using('sca').get(id=id_aluno)

    # Armazena o nome do aluno
    nome_aluno = aluno.nome

    # Armazena a lista das disciplinas já cumpridas pelo aluno, essas podem ter uma das situações abaixo
    # (APROVADO, ISENTO_POR_TRANSFERENCIA, APROVEITAMENTO_CREDITOS, ISENTO, MATRICULA, APROVADO_SEM_NOTA)
    disciplinas_concluidas = []

    periodos_trancamento_total = []
    total_periodos_trancados = 0

    disciplinas_reprovadas = []
    total_reprovacoes_disc = []
    disc_rep_str_nome_codigo = []

    # t_equivalentes = []
    # t_original = []

    periodos_cursados = []
    total_periodos_cursados = 0

    maxreprovacoes = 0
    faixa_reprovacoes = 0
    faixa_integralizacao = 0
    faixa_criticidade = 0

    # Somatório da carga horária das disciplinas eletivas
    # Esta variável inicia zerada e vai sendo incrementada
    carga_horaria_eletivas = 0

    mincreditos = 0
    maxcreditos = 28

    # Retorna todos os itens de histórico escolar do aluno
    historico = Itemhistoricoescolar.objects.using('sca').filter(
        historico_escolar=aluno.historico
    )

    for i in historico:

        id_disciplina = i.disciplina.id

        # Verificação do total de períodos cursados

        p_ano = i.ano
        p_periodo = i.periodo
        p = str(p_ano) + "." + str(p_periodo)

        if p not in periodos_cursados:
            periodos_cursados.append(p)

        total_periodos_cursados = len(periodos_cursados)

        # Verificação das disciplinas cursadas, matriculadas e aprovadas
        if i.situacao in (0, 4, 7, 8, 9, 10, 12):
            disciplinas_concluidas.append(id_disciplina)

            # Verifica se a disciplina é optativa e se positivo extrai a carga horária da mesma
            # O campo optativa no banco de dados é do tipo bit
            if i.disciplina.optativa == b'\x01':
                carga_horaria_eletivas += i.disciplina.cargahoraria

            # TODO: Equivalência de disciplinas
            # Verifica se a disciplina iterada está presente na tabela de disciplinas originais
            """original = Disciplinasoriginais.objects.using('sca').filter(
                disciplinasoriginais=id_disciplina
            )

            bloco = Blocoequivalencia.objects.using('sca').filter(id__in=original)
            t_equivalentes = list(Disciplinasequivalentes.objects.using(
                'sca').filter(bloco__in=bloco).values_list(
                'disciplinasequivalentes', flat=True)
            )
            disciplinas_concluidas.extend(t_equivalentes)

            # Verificação das disciplinas equivalentes (equivalente -> original)
            t_equivalentes = Disciplinasequivalentes.objects.using(
                'sca').filter(disciplinasequivalentes=id_disciplina)
            bloco = Blocoequivalencia.objects.using('sca').filter(
                id__in=t_equivalentes
            )
            t_original = list(Disciplinasoriginais.objects.using('sca').filter(
                bloco__in=bloco).values_list(
                'disciplinasoriginais', flat=True)
            )
            disciplinas_concluidas.extend(t_original)
            """

        # Verificação das disciplinas reprovadas e reprovações
        elif i.situacao in (1, 2, 11):
            try:
                total_reprovacoes_disc[disciplinas_reprovadas.index(id_disciplina)] += 1

            except:
                disciplinas_reprovadas.append(id_disciplina)
                disc_rep_str_nome_codigo.append(i.disciplina.nome + " (" + i.disciplina.codigo + ")")
                total_reprovacoes_disc.append(1)

        # Verifica se a disciplina iterada possui situação de TRANCAMENTO_TOTAL
        # Armazena um dicionário com as disciplinas e suas respectivas situações
        elif i.situacao == 6:
            if p not in periodos_trancamento_total:
                periodos_trancamento_total.append(p)

            total_periodos_trancados = len(periodos_trancamento_total)


    # Ordenação da lista das disciplinas não pendentes
    disciplinas_concluidas.sort()

    # Verifica as disciplinas reprovadas e quantas vezes reprovou cada uma
    for x in range(len(disc_rep_str_nome_codigo)):
        disc_rep_str_nome_codigo[x] = disc_rep_str_nome_codigo[x] + " - " + str(total_reprovacoes_disc[x])

    # CÁLCULOS PARA DEFINIÇÃO DA FAIXA DE CRITICIDADE

    qtd_periodos_min = Versaocurso.objects.using('sca').get(
        id=aluno.versaocurso.id).qtdperiodominimo

    # Parâmetros e cálculo para reprovações por disciplina

    if qtd_periodos_min < 8:
        min_reprovacoes_faixa_laranja = reprovacoes_faixa_laranja_demais_cursos()
        min_reprovacoes_faixa_vermelha = reprovacoes_faixa_vermelha_demais_cursos()
    else:
        min_reprovacoes_faixa_laranja = reprovacoes_faixa_laranja_cursos_8_periodos()
        min_reprovacoes_faixa_vermelha = reprovacoes_faixa_vermelha_cursos_8_periodos()

    if len(total_reprovacoes_disc) != 0:
        max_reprovacoes = max(total_reprovacoes_disc)

    if max_reprovacoes < min_reprovacoes_faixa_laranja:
        faixa_reprovacoes = 0
    elif min_reprovacoes_faixa_laranja <= max_reprovacoes < min_reprovacoes_faixa_vermelha:
        faixa_reprovacoes = 1
    elif max_reprovacoes == min_reprovacoes_faixa_vermelha:
        faixa_reprovacoes = 2
    else:
        faixa_reprovacoes = 3

    # Parâmetros e cálculo para integralização
    min_integralizacao_laranja = formula_inicial_faixa_laranja()
    max_integralizacao_laranja = formula_final_faixa_laranja()
    integralizacao_vermelha = formula_faixa_vermelha()

    # TODO: Ajustar a variável para descrever os trancamentos totais realizados
    total_periodos_cursados -= total_periodos_trancados

    N = qtd_periodos_min / 2
    if total_periodos_cursados < eval(min_integralizacao_laranja):  # 2 * N:
        faixa_integralizacao = 0
    elif total_periodos_cursados <= eval(max_integralizacao_laranja):  # 4 * N - 4:
        faixa_integralizacao = 1
    elif total_periodos_cursados <= eval(integralizacao_vermelha):  # 4 * N - 3:
        faixa_integralizacao = 2
    else:
        faixa_integralizacao = 3

    faixa_criticidade = max(faixa_reprovacoes, faixa_integralizacao)

    if faixa_criticidade == 0:
        criticidade = 'AZUL'
    elif faixa_criticidade == 1:
        criticidade = 'LARANJA'
    elif faixa_criticidade == 2:
        criticidade = 'VERMELHA'
    else:
        criticidade = 'PRETA'

    if faixa_criticidade == 3:
        mincreditos = min_creditos_preta()

    maxcreditos = max_creditos()

    retorno = disciplinas_concluidas, \
              total_reprovacoes_disc, \
              disciplinas_reprovadas, \
              disc_rep_str_nome_codigo, \
              criticidade, \
              mincreditos, \
              maxcreditos, \
              total_periodos_cursados, \
              nome_aluno, \
              total_periodos_trancados, \
              carga_horaria_eletivas

    return retorno
