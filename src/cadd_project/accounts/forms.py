from django import forms
from django.forms import TextInput, PasswordInput, HiddenInput

from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de registro"""

    new_password1 = forms.CharField(widget=forms.PasswordInput(
                    attrs={'class': 'form-control', 'data-rules': 'required',
                           'placeholder': 'Informe a nova senha'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control',
                                          'data-rules': 'required',
                                          'placeholder': 'Informe a matrícula'}),
            'password': PasswordInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a senha'}),
            'first_name': HiddenInput(),
            'last_name': HiddenInput(),
            'email': HiddenInput(),
        }

    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get('username')):
            raise forms.ValidationError("Matrícula já registrada!")
        if (self.cleaned_data.get('password') != self.cleaned_data.get('new_password1')):
            raise forms.ValidationError("Senhas diferentes!")

        return self.cleaned_data
