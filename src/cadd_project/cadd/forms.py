from django import forms

from .models import Horario

#class CategoriaForm(forms.ModelForm):
#    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#    descricao = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
#    class Meta:
#        model = Categoria
#        exclude = (id, 'user',)

class HorarioForm(forms.ModelForm):
    """Classe para o formulário de criação da prévia do horário do semestre subsequente"""

    class Meta:
        model = Horario
        fields = '__all__'
#        exclude = (id, 'user',)

#    def __init__(self, user=None, *args, **kwargs):
#        super(TarefaForm, self).__init__(*args, **kwargs)
#        if user is not None:
#            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
