from django import forms
from .models import Evaluacion,EvaluacionFormalidad,EvaluacionGestionOtorga,EvaluacionDepuracionAntecedentes,EvaluacionIngresoDeDatos
from .models import Errores_agravante
from datetime import date
class EvaluacionForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        initial=date.today
    )

    class Meta:
        model = Evaluacion
        fields = [
            'rut_cliente', 'nombre_ejec', 'login_ejecutivo', 'rut_ejec','sucursal',
            'codigo_sucursal', 'producto', 'monto_solicitado', 'proceso_credito',
            'tipo_cliente', 'fecha',
        ]
        widgets = {
            'rut_cliente': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nombre_ejec': forms.TextInput(attrs={'readonly': 'readonly'}),
            'login_ejecutivo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'rut_ejec': forms.TextInput(attrs={'readonly': 'readonly'}),
            'sucursal': forms.TextInput(attrs={'readonly': 'readonly'}),
            'codigo_sucursal': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'producto': forms.TextInput(attrs={'readonly': 'readonly'}),
            'monto_solicitado': forms.TextInput(attrs={'readonly': 'readonly'}),
            'proceso_credito': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha > date.today(): # type: ignore
            raise forms.ValidationError("La fecha no puede ser en el futuro.")
        return fecha

    def clean_tipo_cliente(self):
        tipo = self.cleaned_data.get('tipo_cliente')
        if not tipo:
            raise forms.ValidationError("Debe seleccionar un tipo de cliente.")
        return tipo
class EvaluacionFormalidadForm(forms.ModelForm):
    class Meta:
        model = EvaluacionFormalidad
        fields = [
            'respuesta_verificacion_laboral',
            'tipo_error_verificacion_laboral',
            'observacion_verificacion',
            'respuesta_estado_situacion',
            'tipo_error_estado_situacion',
            'observacion_estado',
            'respuesta_acreditacion_ingresos',
            'tipo_error_acreditacion_ingresos',
            'observacion_acreditacion',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar filtros por ítem
        self.fields['tipo_error_verificacion_laboral'].queryset = Errores_agravante.objects.filter(item='verificacion_laboral')# type: ignore
        self.fields['tipo_error_estado_situacion'].queryset = Errores_agravante.objects.filter(item='estado_situacion')# type: ignore
        self.fields['tipo_error_acreditacion_ingresos'].queryset = Errores_agravante.objects.filter(item='acreditacion_ingresos')# type: ignore

class EvaluacionGestionOtorgaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionGestionOtorga
        fields = [
            'respuesta_atribuciones',
            'tipo_error_atribuciones',
            'observaciones_atribuciones',
            'respuesta_constitucion_garantia',
            'tipo_error_constitucion_garantia',
            'observaciones_constitucion_garantia',
            'respuesta_condiciones_aprobacion',
            'tipo_error_condiciones_aprobacion',
            'observacion_condicion_aprob',
            'respuesta_cambio_evaAT',
            'tipo_error_cambio_evaAT',
            'observacion_cambioEva',
            'respuesta_deudas_vinculadas',
            'observacion_res_deuda_vincu',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar filtros por ítem
        self.fields['tipo_error_atribuciones'].queryset = Errores_agravante.objects.filter(item='error_atribuciones')# type: ignore
        self.fields['tipo_error_constitucion_garantia'].queryset = Errores_agravante.objects.filter(item='constitucion_garantia')# type: ignore
        self.fields['tipo_error_condiciones_aprobacion'].queryset = Errores_agravante.objects.filter(item='condiciones_aprobacion')# type: ignore
        self.fields['tipo_error_cambio_evaAT'].queryset = Errores_agravante.objects.filter(item='cambio_evaAT')# type: ignore
class EvaluacionDepuracionAntecedentesForm(forms.ModelForm):
    class Meta:
        model = EvaluacionDepuracionAntecedentes
        fields = [
            'respuesta_ingresos_mensuales',
            'tipo_error_ingresos_mensuales',
            'observacion_ingresos_mensuales',
            'respuesta_activo',
            'observacion_activo',
            'respuesta_dividendo_BCH',
            'observacion_dividendo_BCH',
            'respuesta_arriendos',
            'observacion_arriendos',
            'respuesta_cuota_prestamo',
            'observacion_cuota_prestamo',
            'respuesta_renegociado',
            'tipo_error_monto_renegociado',
            'observacion_renegociado',
            'respuesta_otros_egre',
            'observacion_otros_egre',
            'corresponde_compra_cartera', 
            'respuesta_cuota_cp',
            'observacion_cuota_cp',
            'respuesta_cuota_ooii',
            'observacion_cuota_ooii',
            'respuesta_monto_compra_lp',
            'observacion_monto_compra_lp',
            'respuesta_monto_compra_cp',
            'observacion_monto_compra_cp',
            'respuesta_monto_compra_ooii',
            'observacion_monto_compra_ooii',
            'respuesta_monto_compra_sbif',
            'observacion_monto_compra_sbif',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar filtros por ítem
        self.fields['tipo_error_ingresos_mensuales'].queryset = Errores_agravante.objects.filter(item='ingresos_mensuales')# type: ignore
        self.fields['tipo_error_monto_renegociado'].queryset = Errores_agravante.objects.filter(item='monto_renegociado')# type: ignore
        self.fields['corresponde_compra_cartera'].widget = forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')])

class EvaluacionIngresoDeDatosForm(forms.ModelForm):
    class Meta:
        model = EvaluacionIngresoDeDatos
        fields = [
            'respuesta_actividad',
            'observacion_actividad',
            'respuesta_direccion_part',
            'observacion_direccion_part',
            'respuesta_universidad',
            'observacion_universidad',
            'respuesta_fecha_in_empleo',
            'observacion_fecha_in_empleo',
            'respuesta_nivel_educa',
            'observacion_nivel_educa',
            'respuesta_nacionalidad',
            'observacion_nacionalidad',
            'respuesta_tipo_contrato',
            'observacion_tipo_contrato',
            'respuesta_tipo_renta',
            'observacion_tipo_renta',
            'respuesta_carrera_semestre',
            'observacion_carrera_semestre',
            'respuesta_profesion',
            'observacion_profesion',
            'respuesta_estado_civil',
            'observacion_estado_civil',
            ]
        
from django.forms import inlineformset_factory, BaseInlineFormSet

class BaseEvaluacionFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        # Ocultar el checkbox de eliminar
        form.fields['DELETE'].widget = forms.HiddenInput()

FormalidadFormSet = inlineformset_factory(Evaluacion, EvaluacionFormalidad, form=EvaluacionFormalidadForm, formset=BaseEvaluacionFormSet, extra=1)
GestionOtorgaFormSet = inlineformset_factory(Evaluacion, EvaluacionGestionOtorga, form=EvaluacionGestionOtorgaForm, formset=BaseEvaluacionFormSet, extra=1)
DepuracionAntecedentesFormSet = inlineformset_factory(Evaluacion, EvaluacionDepuracionAntecedentes, form=EvaluacionDepuracionAntecedentesForm, formset=BaseEvaluacionFormSet, extra=1)
IngresoDeDatosFormSet = inlineformset_factory(Evaluacion, EvaluacionIngresoDeDatos, form=EvaluacionIngresoDeDatosForm, formset=BaseEvaluacionFormSet, extra=1)