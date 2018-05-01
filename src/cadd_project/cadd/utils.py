from .models import Parametros, Comissao, Membro, Horario, ItemHorario

def linhas_por_pagina():
    """Função que retorna a quantidade de itens por página cadastrada em parâmetros"""

    linhas = 5
    registros = Parametros.objects.filter(id=1).count()
    if registros != 0:
        linhas = Parametros.objects.get(pk=1).defaultitensporpagina
    return linhas
