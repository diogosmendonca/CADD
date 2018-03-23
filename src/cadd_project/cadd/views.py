from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import HorarioForm
from .models import Horario, ItemHorario

# Create your views here.

# Horário
@login_required
def detalhes_horario(request, id_horario):
    horario = get_object_or_404(Horario, id=id_horario) #, user=request.user)
    return render(request, 'cadd/detalhes_horario.html', {'horario': horario})


@login_required
def novo_itemhorario(request):
    if request.method == 'POST':
        form = HorarioForm(user=request.user, data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('cadd/detalhes_horario.html')
        else:
            print(form.errors)
    else:
        form = HorarioForm(user=request.user)
    return render(request, 'cadd/novo_itemhorario.html', {'form': form})

@login_required
def delete_itemhorario(request, id_tarefa):
    tarefa = Tarefa.objects.get(id=id_tarefa)
    if tarefa.user == request.user:
        tarefa.delete()
    else:
        messages.error(request, 'Você não tem permissão para excluir essa tarefa!')
        return render(request, 'cadd/detalhes_horario.html')
    return redirect('')

@login_required
def editar_itemhorario(request, id_tarefa):
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, user=request.user)
    if request.method == 'POST':
        form = TarefaForm(user=request.user, data=request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('cadd/detalhes_horario.html')
    else:
        form = TarefaForm(user=request.user, instance=tarefa)
    return render(request, 'tarefas/nova_tarefa.html', {'form': form})
