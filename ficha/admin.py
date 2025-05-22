from django.contrib import admin
from .models import (
    Errores_agravante,
    UserProfile,
    EvaluacionFormalidad,
    EvaluacionGestionOtorga,
    EvaluacionDepuracionAntecedentes,
    EvaluacionIngresoDeDatos,
    Evaluacion,
    Registro_materialidad
)

admin.site.site_header = 'Admin Ficha Banco de Chile'

# Modelos simples
admin.site.register(Errores_agravante)
admin.site.register(UserProfile)
admin.site.register(Registro_materialidad)
admin.site.register(EvaluacionFormalidad)
admin.site.register(EvaluacionGestionOtorga)
admin.site.register(EvaluacionDepuracionAntecedentes)
admin.site.register(EvaluacionIngresoDeDatos)

# Admin personalizado para Evaluacion
@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['id_evaluacion', 'tipo_cliente', 'nota_final', 'clasificacion', 'tiene_errores']
    actions = ['calcular_nota_final_action']

    @admin.action(description="Calcular nota final y clasificación")
    def calcular_nota_final_action(self, request, queryset):
        for evaluacion in queryset:
            evaluacion.calcular_nota_final()
        self.message_user(request, "Nota final y clasificación recalculadas correctamente.")
        
    def tiene_errores(self, obj):
        cantidad = obj.contar_errores_totales()
        if cantidad > 0:
            return f"Sí ({cantidad} errores)"
        return "No (0 errores)"
    tiene_errores.short_description = "¿Tiene errores?" # type: ignore

