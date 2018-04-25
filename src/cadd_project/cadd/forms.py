from django import forms
from django.forms import TextInput, Textarea, Select, CheckboxInput, HiddenInput, \
                            NumberInput, TimeInput

from .models import Comissao, Membro, Horario, ItemHorario

class ComissaoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de comissões"""

    class Meta:
        model = Comissao
        exclude = (id, )
        widgets = {
            'curso': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'descricao': Textarea(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a descrição'})
        }
        empty_value_display = 'Selecione o curso'


class MembroForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de membros"""

    class Meta:
        model = Membro
        exclude = (id, 'comissao', )
        widgets = {
            'professor': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'portaria': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a portaria'}),
            'presidente': CheckboxInput(attrs={'class': 'form-control'}),
            'ativo': CheckboxInput(attrs={'class': 'form-control'})
#            'comissao': HiddenInput(attrs={'class': 'form-control',
#                                         'default': id_comissao})
        }
        empty_value_display = 'Selecione o professor'


class HorarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de horários"""

    class Meta:
        model = Horario
        exclude = (id, )
        widgets = {
            'curso': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione o curso'}),
            'ano': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 2016, 'max': 2050, 'step': 1}),
            'periodo': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'})
        }


class ItemHorarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de itens de horário"""

    class Meta:
        model = ItemHorario
        exclude = (id, 'horario', )
        widgets = {
            'periodo': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe o periodo'}),
            'diasemana': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'inicio': TimeInput(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'fim': TimeInput(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'departamento': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'turma': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'disciplina': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'professor': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
        }
