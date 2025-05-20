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
        # Verifica si hay errores agravantes en alguno de los formularios
        for form in obj.formalidad.all():
            if form.get_notas_agravantes():
                return True
        for form in obj.gestion_otorga.all():
            if form.get_notas_agravantes():
                return True
        for form in obj.depuracion_antecedentes.all():
            if form.get_notas_agravantes():
                return True
        return False
    tiene_errores.boolean = True
    tiene_errores.short_description = "¿Tiene errores?"
