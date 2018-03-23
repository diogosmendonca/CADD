from django.urls import path

from . import views

app_name = 'cadd'

urlpatterns = [
    path('detalhes-horario/', views.detalhes_horario, name='detalhes_horario'),
    path('novo-itemhorario/', views.novo_itemhorario, name='novo_itemhorario'),
    path('editar-itemhorario/?<id_itemhorario>', views.editar_itemhorario, name='editar_itemhorario'),
    path('delete-itemhorario/?<id_itemhorario>', views.delete_itemhorario, name='delete_itemhorario'),
]
