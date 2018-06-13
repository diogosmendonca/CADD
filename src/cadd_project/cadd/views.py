from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from django.forms import formset_factory

# Models e Forms
from .forms import ParametrosForm, ComissaoForm, MembroForm, HorarioForm, \
                    ItemHorarioForm, PlanoForm, PlanoAtualForm, ReuniaoForm, \
                    ConvocadoForm, DocumentoForm
from .models import Parametros, Comissao, Membro, Horario, ItemHorario, Plano, \
                    ItemPlanoAtual, PlanoFuturo, ItemPlanoFuturo, Reuniao, \
                    Convocacao, Documento
from sca.models import Aluno, Disciplina, Itemhistoricoescolar

# Paginação
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Funções gerais
from .utils import linhas_por_pagina, max_creditos, max_creditos_preta

# Create your views here.

# Configurações do sistema
@login_required
def editar_parametros(request):
    """Função para a edição dos parâmetros do sistema"""

    registros = Parametros.objects.filter(id=1).count()
    if request.method == 'POST':
        if registros != 0:
            parametros = get_object_or_404(Parametros, id=1)
            form = ParametrosForm(request.POST, instance=parametros)
        else:
            form = ParametrosForm(request.POST)
        if form.is_valid():
            form.save()
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
    """Função para a criação de uma nova comissão de apoio"""

    if request.method == 'POST':
        form = ComissaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_comissoes')
    else:
        form = ComissaoForm()
    return render(request, 'cadd/nova_comissao.html', {
                        'form': form,
                        'ativoComissoes': True
                    })

@login_required
def lista_comissoes(request):
    """Função para a listagem das comissões de apoio cadastradas"""

    linhas = linhas_por_pagina()
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
    """Função para a exclusão de uma comissão de apoio"""

    comissao = Comissao.objects.get(id=id_comissao)
    comissao.delete()
    return redirect('cadd:lista_comissoes')

@login_required
def editar_comissao(request, id_comissao):
    """Função para a edição de uma comissão de apoio"""

    comissao = get_object_or_404(Comissao, id=id_comissao)
    if request.method == 'POST':
        form = ComissaoForm(request.POST, instance=comissao)
        if form.is_valid():
            form.save()
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
    """Função para a criação de uma novo membro de uma comissão de apoio"""

    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            comissao = Comissao.objects.get(id=id_comissao)
            f = form.save(commit=False)
            f.comissao = comissao
            f.ativo = True
            f.save()
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
    """Função para a listagem dos membros cadastrados de uma comissões de apoio"""

    linhas = linhas_por_pagina()
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
    """Função para a desativação de um membro de uma comissão de apoio"""
    membro = Membro.objects.get(id=id_membro)
    membro.ativo = False
    membro.save()
#    membro.delete()
    return redirect('cadd:lista_membros', id_comissao)

@login_required
def editar_membro(request, id_membro, id_comissao):
    """Função para a edição de um membro de uma comissão de apoio"""

    membro = get_object_or_404(Membro, id=id_membro)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
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
    """Função para a criação de uma nova previsão de horário"""

    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_horarios')
    else:
        form = HorarioForm()
    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })

@login_required
def lista_horarios(request):
    """Função para a listagem das previsões de horário"""

    linhas = linhas_por_pagina()
    membro = Membro.objects.filter(professor=request.user.first_name).values_list('comissao')
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
    """Função para a exclusão de uma previsão de horário"""

    horario = Horario.objects.get(id=id_horario)
    horario.delete()
    return redirect('cadd:lista_horarios')

@login_required
def editar_horario(request, id_horario):
    """Função para a edição de uma previsão de horário"""

    horario = get_object_or_404(Horario, id=id_horario)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })


# Itens de Horário
@login_required
def novo_itemhorario(request, id_horario):
    """Função para a criação de uma novo item em uma previsão de horário"""

    if request.method == 'POST':
        form = ItemHorarioForm(request.POST)
        if form.is_valid():
            horario = Horario.objects.get(id=id_horario)
            f = form.save(commit=False)
            f.horario = horario
            f.save()
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
    """Função para a listagem dos itens cadastrados em uma previsão de horário"""

    linhas = linhas_por_pagina()
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
    """Função para a exclusão de um item de uma previsão de horário"""

    itemhorario = ItemHorario.objects.get(id=id_itemhorario)
    itemhorario.delete()
    return redirect('cadd:lista_itenshorario', id_horario)

@login_required
def editar_itemhorario(request, id_itemhorario, id_horario):
    """Função para a edição de item de uma previsão de horário"""

    itemhorario = get_object_or_404(ItemHorario, id=id_itemhorario)
    if request.method == 'POST':
        form = ItemHorarioForm(request.POST, instance=itemhorario)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm(instance=itemhorario)
    return render(request, 'cadd/novo_itemhorario.html', {
                        'form': form,
                        'id_horario': id_horario,
                        'ativoHorarios': True
                    })


#Planos de estudo
@login_required
def lista_planos(request):
    """Função para a listagem dos planos de estudo cadastrados"""

    planoAtual = ""
    itensAtual = ""
    planosFuturos = ""
    itensFuturos = ""
    try:
        planoAtual = Plano.objects.get(aluno=request.user.first_name)
        if planoAtual:
            itensAtual = ItemPlanoAtual.objects.filter(plano=planoAtual)
            planosFuturos = PlanoFuturo.objects.filter(plano=planoAtual)  #.order_by(ano, periodo)
        if planosFuturos:
            itensFuturos = ItemPlanoFuturo.objects.filter(planofuturo__in=planosFuturos)   #.order_by(planofuturo)
    except:
        pass

    return render(request, 'cadd/plano_estudos_cadastrado.html', {
                        'ativoPlanos': True,
                        'planoAtual': planoAtual,
                        'itensAtual': itensAtual,
                        'planosFuturos': planosFuturos,
                        'itensFuturos': itensFuturos
                    })

@login_required
def novo_plano_previa(request):
    """Função para a criação de um novo plano de estudos para o
        próximo semestre"""

    aluno = Aluno.objects.using('sca').get(nome__exact=request.user.last_name)
    versaocurso = aluno.versaocurso

#    fields = 'field1', 'field2', 'fieldN'
    disciplinas = Itemhistoricoescolar.objects.using('sca').filter(historico_escolar=aluno.historico, situacao__in=[0, 9, 12]) # disciplinas aprovadas
    aprovadas = list(disciplinas.values_list('disciplina_id', flat=True)) #foradocurso e equivalentes
#    foradocurso = list(disciplinas.exclude(disciplina.versaocurso!=aluno.versaocurso))
    equivalentes = ''
    previas = list(ItemHorario.objects.all().values_list('disciplina', flat=True)) #falta separar por ano e periodo
    # now you have two lists of tuples so you can apply ordinary python comparisons / set operations etc
    rows3 = set(previas) - set(disciplinas)

    criticidade = ''
    reprovadas = ''
    equivalentes = ''
    prerequisitos = ''
    maxcreditosporperiodo = max_creditos()
    maxcreditosporperiodopreta = max_creditos_preta()
    lecionadas = Itemhistoricoescolar.objects.using('sca').filter(historico_escolar=aluno.historico).values_list('disciplina_id', flat=True)
    disciplinasCurso = Disciplina.objects.using('sca').filter(versaocurso=aluno.versaocurso)
    aLecionar = disciplinasCurso.difference(lecionadas)
    podeLecionarnoPeriodo = ItemHorario.objects.filter(disciplina__in=rows3).order_by('diasemana') #.exclude(disciplina__in=lecionadas)    #filter(disciplina=lecionadas[0])
#    listaHorarios = ItemHorario.objects.order_by('inicio').values_list('inicio', flat=True).distinct().exclude(inicio=None)
    listaHorarios = ('07:00', '07:55', '08:50', '09:55', '10:50', '11:45', \
                     '12:40', '13:35', '14:30', '15:35', '16:30', '17:25', \
                     '18:20', '19:10', '20:00', '21:00', '21:50')

    if request.method == 'POST':
        disciplinas = request.POST.get('discip')
        if disciplinas:
            disciplinas = disciplinas.split("_")
            aluno = Aluno.objects.get(id=request.user.first_name)
            plano = Plano.objects.create(ano=2018, periodo=1, situacao='M', aluno=aluno)
            for d in disciplinas:
                disc = int(d)
                itemhorario = ItemHorario.objects.get(id=disc)
                i = ItemPlanoAtual.objects.create(plano=plano, itemhorario=itemhorario)

        return redirect('cadd:lista_planos')
    return render(request, 'cadd/plano_estudos_previa.html', {
                        'ativoPlanos': True,
                        'podeLecionarnoPeriodo': podeLecionarnoPeriodo,
                        'listaHorarios': listaHorarios
                    })

def novo_plano_futuro(request):
    """Função para a criação de um novo plano de estudos para os
        semestres subsequentes"""

    aluno = Aluno.objects.using('sca').get(nome__exact=request.user.last_name)
    lecionadas = Itemhistoricoescolar.objects.using('sca').filter(historico_escolar=aluno.historico).values_list('disciplina_id', flat=True)
    disciplinasCurso = Disciplina.objects.using('sca').filter(versaocurso=aluno.versaocurso)
    aLecionar = disciplinasCurso.difference(lecionadas)

    return render(request, 'cadd/plano_estudos_futuro.html', {
                        'ativoPlanos': True
                    })


# Reuniões
@login_required
def nova_reuniao(request):
    """Função para a criação de uma nova reuniao"""

    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_reunioes')
    else:
        form = ReuniaoForm()
    return render(request, 'cadd/nova_reuniao.html', {
                        'form': form,
                        'ativoReunioes': True
                    })

@login_required
def lista_reunioes(request):
    """Função para a listagem das reuniões agendadas"""

    linhas = linhas_por_pagina()
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
    """Função para o cancelamento de uma reunião"""

    reuniao = Reuniao.objects.get(id=id_reuniao)
    reuniao.situacao = 'C'
    reuniao.save()
    return redirect('cadd:lista_reunioes')

@login_required
def editar_reuniao(request, id_reuniao):
    """Função para a edição de uma reuniao"""

    reuniao = get_object_or_404(Reuniao, id=id_reuniao)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
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
    """Função para a cadastro de um convocado para uma reunião específica"""

    if request.method == 'POST':
        form = ConvocadoForm(request.POST)
        if form.is_valid():
            reuniao = Reuniao.objects.get(id=id_reuniao)
            f = form.save(commit=False)
            f.reuniao = reuniao
            f.save()
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
    """Função para a listagem dos convidados para uma reunião específica"""

    linhas = linhas_por_pagina()
    convocados_list = Convocacao.objects.filter(reuniao=id_reuniao)
    paginator = Paginator(convocados_list, linhas) # Paginação
    page = request.GET.get('page')
    convocados = paginator.get_page(page)
    reuniao = Reuniao.objects.get(id__exact=id_reuniao) # objeto reunião anteriormente requisitado
    return render(request, 'cadd/lista_convocados.html', {
                        'convocados': convocados,
                        'id_reuniao': id_reuniao,
                        'reuniao': reuniao,
                        'ativoReunioes': True
                    })

@login_required
def excluir_convocado(request, id_convocado, id_reuniao):
    """Função para a exclusão de um convocado de uma reunião específica"""

    convocado = Convocacao.objects.get(id=id_convocado)
    convocado.delete()
    return redirect('cadd:lista_convocados', id_reuniao)

@login_required
def editar_convocado(request, id_convocado, id_reuniao):
    """Função para a edição de um convocado para uma reuniao específica"""

    convocado = get_object_or_404(Convocacao, id=id_convocado)
    if request.method == 'POST':
        form = ConvocadoForm(request.POST, instance=convocado)
        if form.is_valid():
            form.save()
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
    """Função para o cadastro de um novo documento"""

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_documentos')
    else:
        form = DocumentoForm()
    return render(request, 'cadd/novo_documento.html', {
                        'form': form,
                        'ativoDocumentos': True
                    })

@login_required
def lista_documentos(request):
    """Função para a listagem dos documentos cadastrados"""

    linhas = linhas_por_pagina()
    documentos_list = Documento.objects.all()
    paginator = Paginator(documentos_list, linhas) # Paginação
    page = request.GET.get('page')
    documentos = paginator.get_page(page)
    return render(request, 'cadd/lista_documentos.html', {
                        'documentos': documentos,
                        'ativoDocumentos': True
                    })

@login_required
def excluir_documento(request, id_documento):
    """Função para a exclusão de um documento"""

    documento = Documento.objects.get(id=id_documento)
    documento.delete()
    return redirect('cadd:lista_documentos')

@login_required
def visualizar_documento(request, id_documento):
    """Função para a visualização de um documento cadastrado"""

    doc = get_object_or_404(Documento, id=id_documento)
    return render(request, 'cadd/visualiza_documento.html', {
                        'doc': doc,
                        'ativoDocumentos': True
                    })
