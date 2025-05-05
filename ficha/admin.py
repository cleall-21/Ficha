from django.contrib import admin
from .models import Errores_agravante,UserProfile,EvaluacionFormalidad,EvaluacionGestionOtorga,EvaluacionDepuracionAntecedentes,EvaluacionIngresoDeDatos
from .models import Evaluacion, Registro_materialidad

admin.site.site_header = 'Admin Ficha Banco de Chile'

# Register your models here.
admin.site.register(Errores_agravante)
admin.site.register(UserProfile)
admin.site.register(Evaluacion)
admin.site.register(Registro_materialidad)
admin.site.register(EvaluacionFormalidad)
admin.site.register(EvaluacionGestionOtorga)
admin.site.register(EvaluacionDepuracionAntecedentes)
admin.site.register(EvaluacionIngresoDeDatos)