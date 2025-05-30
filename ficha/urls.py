from django.urls import path, include
from .views import (
    login, base, index, registro, listar_ejec, reporte,
    carga_materialidad, listar_evaluaciones, detalle_eva,
    delete_evaluacion, buscar_oportunidad, obtener_datos_oportunidad, vista_evaluaciones_api
)

# Importaciones para la API´s
from rest_framework.routers import DefaultRouter
from .views import EvaluacionViewSet, DetalleEvaluacionesViewSet  

# Configuración del router para la API
router = DefaultRouter()
router.register(r'evaluaciones', EvaluacionViewSet)
router.register(r'detalle-evaluaciones', DetalleEvaluacionesViewSet)

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
    path('obtener_oportunidad/<str:rut>/', obtener_datos_oportunidad, name='obtener_oportunidad'),
    path('calculo_nota/', vista_evaluaciones_api, name='notas'),

    # Rutas de la API
    path('', include(router.urls)),
]
