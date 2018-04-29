from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Paginação
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .forms import ComissaoForm, MembroForm, HorarioForm, ItemHorarioForm
from .models import Comissao, Membro, Horario, ItemHorario
from sca.models import Curso

# Create your views here.

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
    return render(request, 'cadd/nova_comissao.html', {'form': form})

@login_required
def lista_comissoes(request):
    """Função para a listagem das comissões de apoio cadastradas"""

    comissoes_list = Comissao.objects.all()
    paginator = Paginator(comissoes_list, 5) # Paginação. Exibe 5 itens por vez
    page = request.GET.get('page')
    comissoes = paginator.get_page(page)
    return render(request, 'cadd/lista_comissoes.html', {'comissoes': comissoes})

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
    else:
        form = ComissaoForm(instance=comissao)
    return render(request, 'cadd/nova_comissao.html', {'form': form})


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
            f.save()
            return redirect('cadd:lista_membros', id_comissao)
    else:
        form = MembroForm()
    return render(request, 'cadd/novo_membro.html', {'form': form, 'id_comissao': id_comissao})

@login_required
def lista_membros(request, id_comissao):
    """Função para a listagem dos membros cadastrados de uma comissões de apoio"""

    membros_list = Membro.objects.all().filter(comissao=id_comissao)
    paginator = Paginator(membros_list, 5) # Paginação. Exibe 5 itens por vez
    page = request.GET.get('page')
    membros = paginator.get_page(page)
    comissao = Comissao.objects.get(id__exact=id_comissao) # objeto comissão anteriormente requisitado
    return render(request, 'cadd/lista_membros.html', {'membros': membros, 'id_comissao': id_comissao, 'comissao': comissao})

@login_required
def excluir_membro(request, id_membro, id_comissao):
    """Função para a exclusão de um membro de uma comissão de apoio"""
    membro = Membro.objects.get(id=id_membro)
    membro.delete()
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
    return render(request, 'cadd/novo_membro.html', {'form': form, 'id_comissao': id_comissao})


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
    return render(request, 'cadd/novo_horario.html', {'form': form})

@login_required
def lista_horarios(request):
    """Função para a listagem das previsões de horário"""

    horarios_list = Horario.objects.all()
    paginator = Paginator(horarios_list, 5) # Paginação. Exibe 5 itens por vez
    page = request.GET.get('page')
    horarios = paginator.get_page(page)
    return render(request, 'cadd/lista_horarios.html', {'horarios': horarios})

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
    return render(request, 'cadd/novo_horario.html', {'form': form})


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
    return render(request, 'cadd/novo_itemhorario.html', {'form': form, 'id_horario': id_horario})

@login_required
def lista_itenshorario(request, id_horario):
    """Função para a listagem dos itens cadastrados em uma previsão de horário"""

    itenshorario_list = ItemHorario.objects.all().filter(horario=id_horario).order_by('periodo', 'disciplina', 'turma')
    paginator = Paginator(itenshorario_list, 5) # Paginação. Exibe 5 itens por vez
    page = request.GET.get('page')
    itenshorario = paginator.get_page(page)
    horario = Horario.objects.get(id__exact=id_horario) # objeto horário anteriormente requisitado
    return render(request, 'cadd/lista_itenshorario.html', {'itenshorario': itenshorario, 'id_horario': id_horario, 'horario': horario})

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
    return render(request, 'cadd/novo_itemhorario.html', {'form': form, 'id_horario': id_horario})
