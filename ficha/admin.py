from django.contrib import admin
from .models import Pilares,Errores_agravante,Parametro,UserProfile
from .models import Evaluacion, DetalleEvaluacion, Registro_materialidad

admin.site.site_header = 'Admin Ficha Banco de Chile'

# Register your models here.
admin.site.register(Pilares)
admin.site.register(Errores_agravante)
admin.site.register(Parametro)
admin.site.register(UserProfile)
admin.site.register(Evaluacion)
admin.site.register(DetalleEvaluacion)
admin.site.register(Registro_materialidad)