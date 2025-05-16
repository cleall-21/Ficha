from django.contrib import admin
from django.urls import path
from .views import login, base, index, registro, listar_ejec, reporte,carga_materialidad,listar_evaluaciones
from .views import detalle_eva,delete_evaluacion,buscar_oportunidad
urlpatterns = [
    path('', login, name='login'),
    path('registro/', registro, name='registro'),
    path('base/', base, name='base'),
    path('index/', index, name='index'),
    path('buscar_oportunidad/', buscar_oportunidad, name='buscar'),
    path('listar_ejec/', listar_ejec, name='listado'),
    path('reporte/', reporte, name='Reporte'),
    path('carga_materialidad/', carga_materialidad, name='carga'),
    path('listar_evaluaciones/', listar_evaluaciones, name='list_form'),
    path('index/<int:id_evaluacion>/', detalle_eva, name='detalle_eva'),
    path('delete_evaluacion/<int:id_evaluacion>/', delete_evaluacion, name='delete_evaluacion'),
]