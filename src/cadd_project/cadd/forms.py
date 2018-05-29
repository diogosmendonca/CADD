from django.forms import BaseFormSet

from django import forms
from django.forms import TextInput, Textarea, Select, CheckboxInput, HiddenInput, \
                            NumberInput, TimeInput, DateInput

from .models import Parametros, Comissao, Membro, Horario, ItemHorario, Plano, \
                            ItemPlanoAtual, Reuniao, Convocacao, Documento
from sca.models import Curso, Professor, Turma, Disciplina, Aluno

class ParametrosForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de parâmetros do sistema"""

    class Meta:
        model = Parametros
        exclude = (id, )
        widgets = {
            'reprovacurso8periodoslaranja': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 1, 'max': 10, 'step': 1,
                                         'empty_label': 'Selecione a quantidade de reprovações'}),
            'reprovademaiscursoslaranja': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 1, 'max': 10, 'step': 1,
                                         'empty_label': 'Selecione a quantidade de reprovações'}),
            'reprovacurso8periodosvermelha': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 1, 'max': 10, 'step': 1,
                                         'empty_label': 'Selecione a quantidade de reprovações'}),
            'reprovademaiscursosvermelha': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 1, 'max': 10, 'step': 1,
                                         'empty_label': 'Selecione a quantidade de reprovações'}),
            'qtdperiodoslaranja': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a fórmula para cálculo da faixa de criticidade Laranja'}),
            'qtdperiodosvermelha': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a fórmula para cálculo da faixa de criticidade Vermelha'}),
            'maxcreditosporperiodopreta': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 1, 'max': 50, 'step': 1,
                                         'empty_label': 'Selecione o máximo de créditos por período'}),
            'defaultitensporpagina': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione o total de itens por página'}),
        }


class ComissaoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de comissões de apoio"""

    def __init__(self,*args,**kwargs):
        super (ComissaoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['curso'].queryset = Curso.objects.using('sca').distinct().order_by('nome')
        self.fields['curso'].empty_label = 'Selecione o curso'

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


class MembroForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de membros de uma comissão de apoio"""

    def __init__(self,*args,**kwargs):
        super (MembroForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['professor'].queryset = Professor.objects.using('sca').distinct().order_by('nome')
        self.fields['professor'].empty_label = 'Selecione o professor'

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
        }


class HorarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de previsão de horários"""

    def __init__(self,*args,**kwargs):
        super (HorarioForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['curso'].queryset = Curso.objects.using('sca').distinct().order_by('nome')
        self.fields['curso'].empty_label = 'Selecione o curso'

    class Meta:
        model = Horario
        exclude = (id, )
        widgets = {
            'curso': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione o curso'}),
            'ano': NumberInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'min': 2016, 'max': 2050, 'step': 1,
                                         'empty_label': 'Selecione o ano'}),
            'periodo': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'})
        }


class ItemHorarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de itens de previsão de horário"""

    def __init__(self,*args,**kwargs):
        super (ItemHorarioForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['turma'].queryset = Turma.objects.using('sca').distinct().order_by('codigo')
        self.fields['disciplina'].queryset = Disciplina.objects.using('sca').distinct().order_by('nome')
        self.fields['professor'].queryset = Professor.objects.using('sca').distinct().order_by('nome')
        self.fields['periodo'].empty_label = 'Selecione o período'
        self.fields['turma'].empty_label = 'Selecione a turma'
        self.fields['disciplina'].empty_label = 'Selecione a disciplina'
        self.fields['professor'].empty_label = 'Selecione o professor'
        self.fields['departamento'].empty_label = 'Selecione o departamento'

    class Meta:
        model = ItemHorario
        exclude = (id, 'horario', )
        widgets = {
            'periodo': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe o periodo'}),
            'turma': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'disciplina': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'professor': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'diasemana': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'}),
            'inicio': TimeInput(attrs={'class': 'form-control',
                                         'placeholder': 'Informe a hora de início'}),
            'fim': TimeInput(attrs={'class': 'form-control',
                                         'placeholder': 'Informe a hora final'}),
            'departamento': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required'})
        }


class PlanoFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["disciplinas"] = forms.CharField()


class PlanoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de plano de estudos"""

    class Meta:
        model = Plano
#        exclude = (id, )
        exclude = '__all__'
        widgets = {
#            'ano': HiddenInput(attrs={data-rules': 'required'}),
#            'periodo': HiddenInput(attrs={data-rules': 'required'}),
#            'situacao': HiddenInput(attrs={data-rules': 'required'}),
#            'aluno': HiddenInput(attrs={data-rules': 'required'}),
        }


class PlanoAtualForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de plano de estudos para o próximo semestre"""

    class Meta:
        model = ItemPlanoAtual
#        exclude = (id, )
        exclude = '__all__'
        widgets = {
#            'plano': HiddenInput(attrs={data-rules': 'required'}),
#            'itemhorario': CheckboxSelectMultiple()
        }


class ReuniaoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de reuniões"""

    def __init__(self,*args,**kwargs):
        super (ReuniaoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['comissao'].queryset = Comissao.objects.distinct().order_by('descricao')
        self.fields['comissao'].empty_label = 'Selecione a comissão de apoio'

    class Meta:
        model = Reuniao
        exclude = (id, 'situacao')
        widgets = {
            'data': DateInput(attrs={'class': 'form-control',
                                         'placeholder': 'Informe a data'}),
            'inicio': TimeInput(attrs={'class': 'form-control',
                                         'placeholder': 'Informe a hora de início'}),
            'local': TextInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe o local'}),
#            'situacao': Select(attrs={'class': 'form-control',
#                                         'data-rules': 'required'}),
            'tipo': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione o tipo'}),
            'anotacao': Textarea(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a anotação'}),
            'comissao': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione a comissão'}),
        }


class ConvocadoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de convocados"""

    def __init__(self,*args,**kwargs):
        super (ConvocadoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['aluno'].queryset = Aluno.objects.using('sca').distinct().order_by('nome')
        self.fields['aluno'].empty_label = 'Selecione o aluno'

    class Meta:
        model = Convocacao
        exclude = (id, 'reuniao')
        widgets = {
            'envioemail': CheckboxInput(attrs={'class': 'form-control'}),
            'presente': CheckboxInput(attrs={'class': 'form-control'}),
            'anotacao': Textarea(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a anotação'}),
            'aluno': Select(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'empty_label': 'Selecione o aluno'}),
        }


class DocumentoForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de documentos"""

    def __init__(self,*args,**kwargs):
        super (DocumentoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['aluno'].queryset = Aluno.objects.using('sca').distinct().order_by('nome')
        self.fields['aluno'].empty_label = 'Selecione o aluno'

    class Meta:
        model = Documento
        exclude = (id, )
