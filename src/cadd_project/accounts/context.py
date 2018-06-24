from django.conf import settings

from cadd.utils import tipo_usuario, periodo_atual
from cadd.models import Perfil, Membro

def context_processors(request):
    ret = {}
    if request.user.is_authenticated:
        usuario = Perfil.objects.get(user=request.user.id)
        ret['matricula'] = usuario.matricula
        ret['idusuario'] = usuario.idusuario
        ret['tipo'] = tipo_usuario(usuario.matricula, 0)
        ret['membro'] = Membro.objects.filter(
                            professor=usuario.idusuario
                        ).values_list('comissao')
        ret['ano'] = periodo_atual()[0]
        ret['periodo'] = periodo_atual()[1]
    else:
        ret['matricula'] = ''
        ret['idusuario'] = ''
        ret['tipo'] = ''
        ret['membro'] = ''
        ret['ano'] = ''
        ret['periodo'] = ''
    return ret
