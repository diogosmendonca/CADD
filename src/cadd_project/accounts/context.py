from django.conf import settings

from cadd.utils import tipo_usuario
from cadd.models import Membro

def context_processors(request):
    ret = {}
    if request.user.is_authenticated:
        ret['tipo'] = tipo_usuario(request.user.username, 0)
        ret['membro'] = Membro.objects.\
            filter(professor=request.user.first_name).values_list('comissao')
    else:
        ret['tipo'] = ''
        ret['membro'] = ''

    return ret
