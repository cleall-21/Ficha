from django import forms
from .models import Registro_materialidad
class SucursalForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha Inicio:',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'invalid': 'Ingrese una fecha válida.'}
    )
    fecha_fin = forms.DateField(
        label='Fecha Fin:',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'invalid': 'Ingrese una fecha válida.'}
    )
    codigo_suc = forms.IntegerField(
        label='Código Sucursal:',
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Debe ser un número válido.'
        }
    )
    nombre_ejecutivo = forms.ChoiceField(
        choices=[],
        label='Nombre Ejecutivo',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        data = self.data or self.initial
        codigo_suc = data.get('codigo_suc')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if codigo_suc:
            try:
                queryset = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
                if fecha_inicio and fecha_fin:
                    queryset = queryset.filter(log_fecha_registro__range=[fecha_inicio, fecha_fin])
                nombres = queryset.values_list('nombre_ejecutivo', flat=True).distinct()
                ##print("Ejecutivos encontrados:", list(nombres))
                self.fields['nombre_ejecutivo'].choices = [('', '---------')] + [(n, n) for n in nombres]
            except (ValueError, TypeError):
                pass

    def clean_codigo_suc(self):
        codigo = self.cleaned_data.get('codigo_suc')
        if codigo <= 0: # type: ignore
            raise forms.ValidationError("El código de sucursal debe ser un número positivo.")
        if not Registro_materialidad.objects.filter(codigo_suc=codigo).exists():
            raise forms.ValidationError("No existe una sucursal con ese código.")
        return codigo

    def clean(self): # type: ignore
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")