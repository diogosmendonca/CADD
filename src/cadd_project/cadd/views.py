from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ComissaoForm, MembroForm, HorarioForm, ItemHorarioForm
from .models import Comissao, Membro, Horario, ItemHorario
from sca.models import Curso

# Create your views here.

# Comissões
@login_required
def nova_comissao(request):
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
    comissoes = Comissao.objects.all()
    return render(request, 'cadd/lista_comissoes.html', {'comissoes': comissoes})

@login_required
def excluir_comissao(request, id_comissao):
    comissao = Comissao.objects.get(id=id_comissao)
    comissao.delete()
    return redirect('cadd:lista_comissoes')

@login_required
def editar_comissao(request, id_comissao):
    comissao = get_object_or_404(Comissao, id=id_comissao)
    if request.method == 'POST':
        form = ComissaoForm(request.POST, instance=comissao)
        if form.is_valid():
            form.save()
#            return redirect('core')
    else:
        form = ComissaoForm(instance=comissao)
    return render(request, 'cadd/nova_comissao.html', {'form': form})


# Membros das Comissões
@login_required
def novo_membro(request, id_comissao):
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
    membros = Membro.objects.all().filter(comissao=id_comissao)
    comissao = Comissao.objects.get(id__exact=id_comissao)
    return render(request, 'cadd/lista_membros.html', {'membros': membros, 'id_comissao': id_comissao, 'comissao': comissao})

@login_required
def excluir_membro(request, id_membro, id_comissao):
    membro = Membro.objects.get(id=id_membro)
    membro.delete()
    return redirect('cadd:lista_membros', id_comissao)

@login_required
def editar_membro(request, id_membro, id_comissao):
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
    horarios = Horario.objects.all()
    return render(request, 'cadd/lista_horarios.html', {'horarios': horarios})

@login_required
def excluir_horario(request, id_horario):
    horario = Horario.objects.get(id=id_horario)
    horario.delete()
    return redirect('cadd:lista_horarios')

@login_required
def editar_horario(request, id_horario):
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
    itenshorario = ItemHorario.objects.all().filter(horario=id_horario).order_by('periodo', 'disciplina', 'turma')
    horario = Horario.objects.get(id__exact=id_horario)
    return render(request, 'cadd/lista_itenshorario.html', {'itenshorario': itenshorario, 'id_horario': id_horario, 'horario': horario})

@login_required
def excluir_itemhorario(request, id_itemhorario, id_horario):
    itemhorario = ItemHorario.objects.get(id=id_itemhorario)
    itemhorario.delete()
    return redirect('cadd:lista_itenshorario', id_horario)

@login_required
def editar_itemhorario(request, id_itemhorario, id_horario):
    itemhorario = get_object_or_404(ItemHorario, id=id_itemhorario)
    if request.method == 'POST':
        form = ItemHorarioForm(request.POST, instance=itemhorario)
        if form.is_valid():
            form.save()
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm(instance=itemhorario)
    return render(request, 'cadd/novo_itemhorario.html', {'form': form, 'id_horario': id_horario})
