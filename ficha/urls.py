from django.contrib import admin
from django.urls import path
from .views import login, base, index, registro, listar_ejec, reporte,carga_materialidad,listar_evaluaciones
from .views import form_formalidad,detalle_eva,complete_evaluacion,delete_evaluacion
urlpatterns = [
    path('', login, name='login'),
    path('registro/', registro, name='registro'),
    path('base/', base, name='base'),
    path('index/', index, name='index'),
    path('listar_ejec/', listar_ejec, name='Listado'),
    path('reporte/', reporte, name='Reporte'),
    path('carga_materialidad/', carga_materialidad, name='Carga'),
    path('form_formalidad/', form_formalidad, name='form_formalidad'),
    path('listar_evaluaciones/', listar_evaluaciones, name='list_form'),
    path('form_formalidad/<int:id_formalidad>/', detalle_eva, name='detalle_eva'),
    path('complete_evaluacion/<int:id_formalidad>/', complete_evaluacion, name='complete_evaluacion'),
    path('delete_evaluacion/<int:id_formalidad>/', delete_evaluacion, name='delete_evaluacion'),
]