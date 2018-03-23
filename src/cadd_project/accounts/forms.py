from django import forms
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    """Classe de uso do sistema para o formulário de registro"""
    
    class Meta:
        model = User
        fields = ('username', 'password')
