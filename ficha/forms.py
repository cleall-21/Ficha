from django import forms
from .models import Registro_materialidad

class SucursalForm(forms.Form):
    codigo_suc = forms.IntegerField(label='Código Sucursal:')
    nombre_ejecutivo = forms.ModelChoiceField(
        queryset=Registro_materialidad.objects.none(),  # Inicialmente vacío
        label='Nombre Ejecutivo',
        required=False
    )
    fecha_inicio = forms.DateField(label='Fecha Inicio:', required=False)
    fecha_fin = forms.DateField(label='Fecha Fin:', required=False)

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        if 'codigo_suc' in self.data:
            try:
                codigo_suc = int(self.data.get('codigo_suc'))
                fecha_inicio = self.data.get('fecha_inicio')
                fecha_fin = self.data.get('fecha_fin')
                queryset = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
                if fecha_inicio and fecha_fin:
                    queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
                self.fields['nombre_ejecutivo'].queryset = queryset.values_list('nombre_ejecutivo', flat=True).distinct()
            except (ValueError, TypeError):
                pass  # Manejar el caso en que codigo_suc no sea un entero válido
        elif self.initial.get('codigo_suc'):
            codigo_suc = self.initial.get('codigo_suc')
            fecha_inicio = self.initial.get('fecha_inicio')
            fecha_fin = self.initial.get('fecha_fin')
            queryset = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
            if fecha_inicio and fecha_fin:
                queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
            self.fields['nombre_ejecutivo'].queryset = queryset.values_list('nombre_ejecutivo', flat=True).distinct()
