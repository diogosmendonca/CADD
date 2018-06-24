from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Paginação
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Models e Forms
from .forms import ParametrosForm, ComissaoForm, MembroForm, HorarioForm, \
                    ItemHorarioForm, AvaliaPlanoForm, ReuniaoForm, \
                    ConvocadoForm, DocumentoForm
from .models import Parametros, Comissao, Membro, Horario, ItemHorario, Plano, \
                    ItemPlanoAtual, PlanoFuturo, ItemPlanoFuturo, Reuniao, \
                    Convocacao, Documento, Perfil
from sca.models import Aluno, Disciplina, Itemhistoricoescolar, Versaocurso, \
                    Curso, Disciplinasoriginais, Blocoequivalencia, \
                    Disciplinasequivalentes

# Funções gerais
from .utils import reprovacoes_faixa_laranja_cursos_8_periodos, \
                    reprovacoes_faixa_vermelha_cursos_8_periodos, \
                    reprovacoes_faixa_laranja_demais_cursos, \
                    reprovacoes_faixa_vermelha_demais_cursos, \
                    formula_inicial_faixa_laranja, formula_final_faixa_laranja, \
                    formula_faixa_vermelha, max_creditos, max_creditos_preta, \
                    linhas_por_pagina, nome_sigla_curso, versao_curso, vida_academica, \
                    excluir_arquivo

# Create your views here.

# Configurações do sistema
@login_required
def editar_parametros(request):
    """
    Função para a edição dos parâmetros do sistema
    """

    registros = Parametros.objects.filter(id=1).count()
    if request.method == 'POST':
        if registros != 0:
            parametros = get_object_or_404(Parametros, id=1)
            form = ParametrosForm(request.POST, instance=parametros)
        else:
            form = ParametrosForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Parâmetro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('home')
    else:
        if registros != 0:
            parametros = get_object_or_404(Parametros, id=1)
            form = ParametrosForm(instance=parametros)
        else:
            form = ParametrosForm()

    return render(request, 'cadd/configuracoes.html', {
                        'form': form,
                        'ativoConfiguracoes': True
                    })


# Comissões de apoio
@login_required
def nova_comissao(request):
    """
    Função para a criação de uma nova comissão de apoio
    """

    if request.method == 'POST':
        form = ComissaoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Comissão salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_comissoes')
    else:
        form = ComissaoForm()

    return render(request, 'cadd/nova_comissao.html', {
                        'form': form,
                        'ativoComissoes': True
                    })

@login_required
def lista_comissoes(request):
    """
    Função para a listagem das comissões de apoio cadastradas
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    comissoes_list = Comissao.objects.all()
    paginator = Paginator(comissoes_list, linhas) # Paginação
    page = request.GET.get('page')
    comissoes = paginator.get_page(page)

    return render(request, 'cadd/lista_comissoes.html', {
                        'comissoes': comissoes,
                        'ativoComissoes': True
                    })

@login_required
def excluir_comissao(request, id_comissao):
    """
    Função para a exclusão de uma comissão de apoio
    """

    comissao = Comissao.objects.get(id=id_comissao)
    try:
        comissao.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'A exclusão não foi realizada! Para isso, exclua primeiramente seus membros.')

    return redirect('cadd:lista_comissoes')

@login_required
def editar_comissao(request, id_comissao):
    """
    Função para a edição de uma comissão de apoio
    """

    comissao = get_object_or_404(Comissao, id=id_comissao)
    if request.method == 'POST':
        form = ComissaoForm(request.POST, instance=comissao)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Comissão salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_comissoes')
    else:
        form = ComissaoForm(instance=comissao)

    return render(request, 'cadd/nova_comissao.html', {
                        'form': form,
                        'ativoComissoes': True
                    })


# Membros das Comissões de apoio
@login_required
def novo_membro(request, id_comissao):
    """
    Função para a criação de uma novo membro de uma comissão de apoio
    """

    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            comissao = Comissao.objects.get(id=id_comissao)
            f = form.save(commit=False)
            f.comissao = comissao
            f.ativo = True
            try:
                form.save()
                messages.success(request, 'Membro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_membros', id_comissao)
    else:
        form = MembroForm()

    return render(request, 'cadd/novo_membro.html', {
                        'form': form,
                        'id_comissao': id_comissao,
                        'ativoComissoes': True
                    })

@login_required
def lista_membros(request, id_comissao):
    """
    Função para a listagem dos membros cadastrados de uma comissões de apoio
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    membros_list = Membro.objects.all().filter(comissao=id_comissao)
    paginator = Paginator(membros_list, linhas) # Paginação
    page = request.GET.get('page')
    membros = paginator.get_page(page)
    # objeto comissão anteriormente requisitado
    comissao = Comissao.objects.get(id__exact=id_comissao)

    return render(request, 'cadd/lista_membros.html', {
                        'membros': membros,
                        'id_comissao': id_comissao,
                        'comissao': comissao,
                        'ativoComissoes': True
                    })

@login_required
def excluir_membro(request, id_membro, id_comissao):
    """
    Função para a desativação de um membro de uma comissão de apoio
    """

    membro = Membro.objects.get(id=id_membro)
    membro.ativo = False
    try:
        membro.save()
        messages.success(request, 'Membro desativado com sucesso!')
    except:
        messages.error(request, 'Houve algum problema técnico e a desativamento não foi realizado!')

    return redirect('cadd:lista_membros', id_comissao)

@login_required
def editar_membro(request, id_membro, id_comissao):
    """
    Função para a edição de um membro de uma comissão de apoio
    """

    membro = get_object_or_404(Membro, id=id_membro)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Membro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_membros', id_comissao)
    else:
        form = MembroForm(instance=membro)

    return render(request, 'cadd/novo_membro.html', {
                        'form': form,
                        'id_comissao': id_comissao,
                        'ativoComissoes': True
                    })


# Horários
@login_required
def novo_horario(request):
    """
    Função para a criação de uma nova previsão de horário
    """

    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_horarios')
    else:
        form = HorarioForm()

    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })

@login_required
def lista_horarios(request):
    """
    Função para a listagem das previsões de horário
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    membro = Membro.objects.filter(professor=usuario.idusuario).values_list('comissao')
    comissoes = Comissao.objects.filter(id__in=membro).values_list('curso')
    horarios_list = Horario.objects.filter(curso__in=comissoes)
    paginator = Paginator(horarios_list, linhas) # Paginação
    page = request.GET.get('page')
    horarios = paginator.get_page(page)

    return render(request, 'cadd/lista_horarios.html', {
                        'horarios': horarios,
                        'ativoHorarios': True
                    })

@login_required
def excluir_horario(request, id_horario):
    """
    Função para a exclusão de uma previsão de horário
    """

    horario = Horario.objects.get(id=id_horario)
    try:
        horario.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'A exclusão não foi realizada! Para isso, exclua primeiramente seus itens de horário.')

    return redirect('cadd:lista_horarios')

@login_required
def editar_horario(request, id_horario):
    """
    Função para a edição de uma previsão de horário
    """

    horario = get_object_or_404(Horario, id=id_horario)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_horarios')
    else:
        form = HorarioForm(instance=horario)

    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })


# Itens de Horário
@login_required
def novo_itemhorario(request, id_horario):
    """
    Função para a criação de uma novo item em uma previsão de horário
    """

    if request.method == 'POST':
        form = ItemHorarioForm(request.POST)
        if form.is_valid():
            horario = Horario.objects.get(id=id_horario)
            f = form.save(commit=False)
            f.horario = horario
            try:
                f.save()
                messages.success(request, 'Item de horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm()

    return render(request, 'cadd/novo_itemhorario.html', {
                        'form': form,
                        'id_horario': id_horario,
                        'ativoHorarios': True
                    })

@login_required
def lista_itenshorario(request, id_horario):
    """
    Função para a listagem dos itens cadastrados em uma previsão de horário
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    itenshorario_list = ItemHorario.objects.all().filter(horario=id_horario).order_by('periodo', 'disciplina', 'turma')
    paginator = Paginator(itenshorario_list, linhas) # Paginação
    page = request.GET.get('page')
    itenshorario = paginator.get_page(page)
    # objeto horário anteriormente requisitado
    horario = Horario.objects.get(id__exact=id_horario)

    return render(request, 'cadd/lista_itenshorario.html', {
                        'itenshorario': itenshorario,
                        'id_horario': id_horario,
                        'horario': horario,
                        'ativoHorarios': True
                    })

@login_required
def excluir_itemhorario(request, id_itemhorario, id_horario):
    """
    Função para a exclusão de um item de uma previsão de horário
    """

    itemhorario = ItemHorario.objects.get(id=id_itemhorario)
    try:
        itemhorario.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão não foi realizada!')

    return redirect('cadd:lista_itenshorario', id_horario)

@login_required
def editar_itemhorario(request, id_itemhorario, id_horario):
    """
    Função para a edição de item de uma previsão de horário
    """

    itemhorario = get_object_or_404(ItemHorario, id=id_itemhorario)
    if request.method == 'POST':
        form = ItemHorarioForm(request.POST, instance=itemhorario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Item de horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm(instance=itemhorario)

    return render(request, 'cadd/novo_itemhorario.html', {
                        'form': form,
                        'id_horario': id_horario,
                        'ativoHorarios': True
                    })


# Reuniões
@login_required
def nova_reuniao(request):
    """
    Função para a criação de uma nova reuniao
    """

    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reunião salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_reunioes')
    else:
        form = ReuniaoForm()

    return render(request, 'cadd/nova_reuniao.html', {
                        'form': form,
                        'ativoReunioes': True
                    })

@login_required
def lista_reunioes(request):
    """
    Função para a listagem das reuniões agendadas
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    reunioes_list = Reuniao.objects.all()
    paginator = Paginator(reunioes_list, linhas) # Paginação
    page = request.GET.get('page')
    reunioes = paginator.get_page(page)

    return render(request, 'cadd/lista_reunioes.html', {
                        'reunioes': reunioes,
                        'ativoReunioes': True
                    })

@login_required
def excluir_reuniao(request, id_reuniao):
    """
    Função para o cancelamento de uma reunião
    """

    reuniao = Reuniao.objects.get(id=id_reuniao)
    reuniao.situacao = 'C'
    try:
        reuniao.save()
        messages.success(request, 'Reunião cancelada com sucesso!')
    except:
        messages.error(request, 'Houve algum problema técnico e a cancelamento não foi realizado!')

    return redirect('cadd:lista_reunioes')

@login_required
def editar_reuniao(request, id_reuniao):
    """
    Função para a edição de uma reunião
    """

    reuniao = get_object_or_404(Reuniao, id=id_reuniao)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reunião salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)

    return render(request, 'cadd/nova_reuniao.html', {
                        'form': form,
                        'ativoReunioes': True
                    })


# Convocados às reuniões
@login_required
def novo_convocado(request, id_reuniao):
    """
    Função para a cadastro de um convocado para uma reunião específica
    """

    if request.method == 'POST':
        form = ConvocadoForm(request.POST)
        if form.is_valid():
            reuniao = Reuniao.objects.get(id=id_reuniao)
            f = form.save(commit=False)
            f.reuniao = reuniao
            f.envioemail = False
            f.presente = False
            try:
                f.save()
                messages.success(request, 'Convocado salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_convocados', id_reuniao)
    else:
        form = ConvocadoForm()

    return render(request, 'cadd/novo_convocado.html', {
                        'form': form,
                        'id_reuniao': id_reuniao,
                        'ativoReunioes': True
                    })

@login_required
def lista_convocados(request, id_reuniao):
    """
    Função para a listagem dos convidados para uma reunião específica
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    convocados_list = Convocacao.objects.filter(reuniao=id_reuniao)
    # Paginação
    paginator = Paginator(convocados_list, linhas)
    page = request.GET.get('page')
    convocados = paginator.get_page(page)
    # objeto reunião anteriormente requisitado
    reuniao = Reuniao.objects.get(id__exact=id_reuniao)

    return render(request, 'cadd/lista_convocados.html', {
                        'convocados': convocados,
                        'id_reuniao': id_reuniao,
                        'reuniao': reuniao,
                        'ativoReunioes': True
                    })

@login_required
def excluir_convocado(request, id_convocado, id_reuniao):
    """
    Função para a exclusão de um convocado de uma reunião específica
    """

    convocado = Convocacao.objects.get(id=id_convocado)
    try:
        convocado.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão não foi realizada!')

    return redirect('cadd:lista_convocados', id_reuniao)

@login_required
def editar_convocado(request, id_convocado, id_reuniao):
    """
    Função para a edição de um convocado para uma reuniao específica
    """

    convocado = get_object_or_404(Convocacao, id=id_convocado)
    if request.method == 'POST':
        form = ConvocadoForm(request.POST, instance=convocado)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Convocado salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_convocados', id_reuniao)
    else:
        form = ConvocadoForm(instance=convocado)

    return render(request, 'cadd/novo_convocado.html', {
                        'form': form,
                        'id_reuniao': id_reuniao,
                        'ativoReunioes': True
                    })

# Documentos
@login_required
def novo_documento(request):
    """
    Função para o cadastro de um novo documento
    """

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Documento salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e a salvamento não foi realizado!')
            return redirect('cadd:lista_documentos')
    else:
        form = DocumentoForm()

    return render(request, 'cadd/novo_documento.html', {
                        'form': form,
                        'ativoDocumentos': True
                    })

@login_required
def lista_documentos(request):
    """
    Função para a listagem dos documentos cadastrados
    """

    usuario = Perfil.objects.get(user=request.user.id)
    # Paginação
    linhas = linhas_por_pagina(usuario.idusuario)
    documentos_list = Documento.objects.all()
    paginator = Paginator(documentos_list, linhas)
    page = request.GET.get('page')
    documentos = paginator.get_page(page)

    return render(request, 'cadd/lista_documentos.html', {
                        'documentos': documentos,
                        'ativoDocumentos': True
                    })

@login_required
def excluir_documento(request, id_documento):
    """
    Função para a exclusão de um documento
    """

    documento = Documento.objects.get(id=id_documento)
    try:
        documento.delete()
        excluir_arquivo(documento.indice)
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão não foi realizada!')

    return redirect('cadd:lista_documentos')

#@login_required
#def visualizar_documento(request, id_documento):
#    """
#    Função para a visualização de um documento cadastrado
#    """
#
#    doc = get_object_or_404(Documento, id=id_documento)
#    return render(request, 'cadd/visualiza_documento.html', {
#                        'doc': doc,
#                        'ativoDocumentos': True
#                    })


#Planos de estudo
@login_required
def lista_planos(request):
    """
    Função para a listagem dos planos de estudo cadastrados
    """

    planoAtual = ""
    itensAtual = ""
    planosFuturos = ""
    itensFuturos = ""
    avaliacao = ""
    try:
        planoAtual = Plano.objects.get(aluno=request.user.first_name)
        if planoAtual:
            itensAtual = ItemPlanoAtual.objects.filter(plano=planoAtual)
            planosFuturos = PlanoFuturo.objects.filter(plano=planoAtual)  #.order_by(ano, periodo)
        if planosFuturos:
            itensFuturos = ItemPlanoFuturo.objects.filter(planofuturo__in=planosFuturos)   #.order_by(planofuturo)
    except:
        pass

    avaliacao = planoAtual.avaliacao

    return render(request, 'cadd/lista_plano_estudos.html', {
                        'ativoPlanos': True,
                        'planoAtual': planoAtual,
                        'itensAtual': itensAtual,
                        'planosFuturos': planosFuturos,
                        'itensFuturos': itensFuturos,
                        'avaliacao': avaliacao,
                    })

@login_required
def novo_plano_previa(request):
    """
    Função para a criação de um novo plano de estudos para o
    próximo semestre
    """
    """TODO: Faltam os pré-requisitos na ajuda à criação do plano"""

    prerequisitos = ''

    # processamento da vida acadêmica do aluno logado
    vidaacademica = vida_academica(request)
    # Verificação do nome do curso, versão do curso e faixa de criticidade
    nomecurso = nome_sigla_curso(request.user.first_name)[0]
    versaocurso = versao_curso(request)
    criticidade = vidaacademica[4]
    maxcreditos = vidaacademica[5]
    periodos = vidaacademica[6]
    plano = 0

    aluno = Aluno.objects.get(id=request.user.first_name)
    # Prévias e afins
    previas = list(ItemHorario.objects.all().values_list('disciplina', flat=True).exclude(disciplina__in=vidaacademica[0])) #falta separar por ano e periodo
    previas.sort()
    podeLecionarnoPeriodo = ItemHorario.objects.filter(disciplina__in=previas).order_by('diasemana') #.exclude(disciplina__in=lecionadas)    #filter(disciplina=lecionadas[0])
    listaHorarios = ('07:00', '07:55', '08:50', '09:55', '10:50', '11:45', \
                     '12:40', '13:35', '14:30', '15:35', '16:30', '17:25', \
                     '18:20', '19:10', '20:00', '21:00', '21:50')

    if request.method == 'POST':
        disciplinas = request.POST.get('discip')
        if disciplinas:
            disciplinas = disciplinas.split("_")
            try:
                plano = Plano.objects.get(ano=2018, periodo=1, aluno=aluno)
            except:
                plano = Plano.objects.create(ano=2018, periodo=1, situacao='M', aluno=aluno)
            for d in disciplinas:
                disc = int(d)
                itemhorario = ItemHorario.objects.get(id=disc)
                i = ItemPlanoAtual.objects.create(plano=plano, itemhorario=itemhorario)

    return render(request, 'cadd/novo_plano_estudos_atual.html', {
                        'ativoPlanos': True,
                        'ativoPlanos2': True,
                        'podeLecionarnoPeriodo': podeLecionarnoPeriodo,
                        'listaHorarios': listaHorarios,
                        'criticidade': criticidade,
                        'maxcreditos': maxcreditos,
                        'nomecurso': nomecurso,
                        'versaocurso': versaocurso,
                        'periodos': periodos,
                    })

@login_required
def novo_plano_futuro(request):
    """
    Função para a criação de um novo plano de estudos para os
    semestres subsequentes
    """
    """TODO: Falta ver as disciplinas da prévia e seus equivalentes"""

    prerequisitos = ''

    # processamento da vida acadêmica do aluno logado
    vidaacademica = vida_academica(request)
    # Verificação do nome do curso, versão do curso e faixa de criticidade
    versaocurso = versao_curso(request)
    criticidade = vidaacademica[4]
    maxcreditos = vidaacademica[5]
    periodos = vidaacademica[6]
    plano = 1

    # Prévias e afins
    aluno = Aluno.objects.using('sca').get(nome__exact=request.user.last_name)
    aprovadas = vidaacademica[0]
    aLecionar = Disciplina.objects.using('sca').exclude(id__in=aprovadas).filter(versaocurso=aluno.versaocurso).order_by('optativa', 'departamento')

#    if request.method == 'POST':
#        disciplinas = request.POST.get('discip')
#        if disciplinas:
#            plano = 1
#            disciplinas = disciplinas.split("_")
#            for d in disciplinas:
#                ano = 2018
#                periodo = 1
#                disc = int(d)
#                plano = PlanoFuturo.objects.create(ano=ano, periodo=periodo, plano=plano)
#                i = ItemPlanoFuturo.objects.create(planofuturo=plano, disciplina=disc)

#        return redirect('cadd:lista_planos')

    return render(request, 'cadd/novo_plano_estudos_futuro.html', {
                        'ativoPlanos': True,
                        'ativoPlanos3': True,
                        'aLecionar': aLecionar,
                        'plano': plano
                    })

@login_required
def lista_planos_avaliar(request):
    """
    Função para a listagem dos alunos e seus planos de estudo cadastrados
    """

    usuario = Perfil.objects.get(user=request.user.id)
#    matricula = request.user.username
    siglacurso = nome_sigla_curso(usuario.idusuario)[1]

#    aluno = Aluno.objects.using('sca').get(nome__exact=request.user.last_name)

    return render(request, 'cadd/lista_plano_estudos_avaliar.html', {
                        'ativoPlanos': True,
#                        'matricula': matricula,
                        'siglacurso': siglacurso,
#                        'aluno': aluno,
                    })

@login_required
def avalia_plano(request, id_aluno):
    """
    Função para a avaliação do plano de estudos dos alunos pelos membros
    das comissões
    """

    # Variáveis
    versaocurso = ""
    criticidade = ""
    periodos = ""
    reprovadas = ""
    planoAtual = ""
    itensAtual = ""
    planosFuturos = ""
    itensFuturos = ""
    avaliacao = ""
    # Processamento da vida acadêmica do aluno logado e obtidos o nome do aluno,
    # versão do curso, faixa de criticidade, periodos, disciplinas reprovadas
    vidaacademica = vida_academica(id_aluno)
    aluno = vidaacademica[7]
    criticidade = vidaacademica[4]
    periodos = vidaacademica[6]
    reprovadas = vidaacademica[3]
    versaocurso = versao_curso(id_aluno)

    # Planos atual e futuro para visualização
    try:
        planoAtual = Plano.objects.get(aluno=id_aluno, ano=2018, periodo=1)
        if planoAtual:
            itensAtual = ItemPlanoAtual.objects.filter(plano=planoAtual)
            planosFuturos = PlanoFuturo.objects.filter(plano=planoAtual)  #.order_by(ano, periodo)
        if planosFuturos:
            itensFuturos = ItemPlanoFuturo.objects.filter(planofuturo__in=planosFuturos)   #.order_by(planofuturo)
    except:
        pass

    if planoAtual.avaliacao:
        avaliacao = planoAtual.avaliacao

    if request.method == 'POST':
        t_avaliacao = request.POST.get('avaliacao')
        if t_avaliacao:
            planoAtual.avaliacao = t_avaliacao
            planoAtual.situacao = 'A'
            planoAtual.save()

    return render(request, 'cadd/avalia_plano_estudos.html', {
                        'aluno': aluno,
                        'versaocurso': versaocurso,
                        'periodos': periodos,
                        'criticidade': criticidade,
                        'reprovadas': reprovadas,
                        'planoAtual': planoAtual,
                        'itensAtual': itensAtual,
                        'planosFuturos': planosFuturos,
                        'itensFuturos': itensFuturos,
                        'avaliacao': avaliacao,
                    })
