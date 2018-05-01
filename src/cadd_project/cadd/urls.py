from django.urls import path

from . import views

app_name = 'cadd'
urlpatterns = [
    path('editar-parametros/', views.editar_parametros, name='editar_parametros'),

    path('lista-comissoes/', views.lista_comissoes, name='lista_comissoes'),
    path('nova-comissao/', views.nova_comissao, name='nova_comissao'),
    path('editar-comissao/?<id_comissao>', views.editar_comissao, name='editar_comissao'),
    path('excluir-comissao/?<id_comissao>', views.excluir_comissao, name='excluir_comissao'),

    path('lista-membros/?<id_comissao>', views.lista_membros, name='lista_membros'),
    path('novo-membro/?<id_comissao>', views.novo_membro, name='novo_membro'),
    path('editar-membro/?<id_membro>&<id_comissao>', views.editar_membro, name='editar_membro'),
    path('excluir-membro/?<id_membro>&<id_comissao>', views.excluir_membro, name='excluir_membro'),

    path('lista-horarios/', views.lista_horarios, name='lista_horarios'),
    path('novo-horario/', views.novo_horario, name='novo_horario'),
    path('editar-horario/?<id_horario>', views.editar_horario, name='editar_horario'),
    path('excluir-horario/?<id_horario>', views.excluir_horario, name='excluir_horario'),

    path('lista-itenshorario/?<id_horario>', views.lista_itenshorario, name='lista_itenshorario'),
    path('novo-itemhorario/?<id_horario>', views.novo_itemhorario, name='novo_itemhorario'),
    path('editar-itemhorario/?<id_itemhorario>&<id_horario>', views.editar_itemhorario, name='editar_itemhorario'),
    path('excluir-itemhorario/?<id_itemhorario>&<id_horario>', views.excluir_itemhorario, name='excluir_itemhorario'),
]
