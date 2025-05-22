from django import forms
from django.forms import inlineformset_factory
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
        fields = ['tipo_cliente', 'fecha', 'nota_final', 'clasificacion']


    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha > date.today():# type: ignore
            raise forms.ValidationError("La fecha no puede ser en el futuro.")
        return fecha

    def clean_tipo_cliente(self):
        tipo = self.cleaned_data.get('tipo_cliente')
        if not tipo:
            raise forms.ValidationError("Debe seleccionar un tipo de cliente.")
        return tipo

    def clean_nota_final(self):
        nota = self.cleaned_data.get('nota_final')
        if nota is None:
            raise forms.ValidationError("Debe ingresar una nota.")
        if nota < 0 or nota > 5:
            raise forms.ValidationError("La nota debe estar entre 0 y 5.")
        return nota

    def clean_clasificacion(self):
        clasificacion = self.cleaned_data.get('clasificacion')
        if not clasificacion:
            raise forms.ValidationError("Debe ingresar una clasificación.")
        if len(clasificacion.strip()) < 3:
            raise forms.ValidationError("La clasificación debe tener al menos 3 caracteres.")
        return clasificacion

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
            'observaciones_revision_credito',
            'respuesta_contribucion_garantia',
            'tipo_error_contribucion_garantia',
            'observaciones_contribucion_garantia',
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
        self.fields['tipo_error_contribucion_garantia'].queryset = Errores_agravante.objects.filter(item='contribucion_garantia')# type: ignore
        self.fields['tipo_error_condiciones_aprobacion'].queryset = Errores_agravante.objects.filter(item='condiciones_aprobacion')# type: ignore
        self.fields['tipo_error_cambio_evaAT'].queryset = Errores_agravante.objects.filter(item='cambio_evaAT')# type: ignore
class EvaluacionDepuracionAntecedentesForm(forms.ModelForm):
    class Meta:
        model = EvaluacionDepuracionAntecedentes
        fields = [
            'respuesta_ingresos_mensuales',
            'tipo_error_ingresos_mensuales',
            'obs_ingresos_mensuales_dice',
            'obs_ingresos_mensuales_debe',
            'observacion_ingresos_mensuales',
            'respuesta_activo',
            'obs_activo_dice',
            'obs_activo_debe',
            'observacion_activo',
            'respuesta_dividendo_BCH',
            'obs_dividendo_BCH_dice',
            'obs_dividendo_BCH_debe',
            'observacion_dividendo_BCH',
            'respuesta_arriendos',
            'obs_arriendos_dice',
            'obs_arriendos_debe',
            'observacion_arriendos',
            'respuesta_cuota_prestamo',
            'obs_cuota_prestamo_dice',
            'obs_cuota_prestamo_debe',
            'observacion_cuota_prestamo',
            'respuesta_otros_egre',
            'obs_otros_egre_dice',
            'obs_otros_egre_debe',
            'observacion_otros_egre',
            'respuesta_renegociado',
            'tipo_error_monto_renegociado',
            'obs_renegociado_dice',
            'obs_renegociado_debe',
            'observacion_renegociado',
            'respuesta_cuota_cp',
            'obs_cuota_cp_dice',
            'obs_cuota_cp_debe',
            'observacion_cuota_cp',
            'respuesta_cuota_ooii',
            'obs_cuota_ooii_dice',
            'obs_cuota_ooii_debe',
            'observacion_cuota_ooii',
            'respuesta_monto_compra_lp',
            'obs_monto_compra_lp_dice',
            'obs_monto_compra_lp_debe',
            'observacion_monto_compra_lp',
            'respuesta_monto_compra_cp',
            'obs_monto_compra_cp_dice',
            'obs_monto_compra_cp_debe',
            'observacion_monto_compra_cp',
            'respuesta_monto_compra_ooii',
            'obs_monto_compra_ooii_dice',
            'obs_monto_compra_ooii_debe',
            'observacion_monto_compra_ooii',
            'respuesta_monto_compra_sbif',
            'obs_monto_compra_sbif_dice',
            'obs_monto_compra_sbif_debe',
            'observacion_monto_compra_sbif',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar filtros por ítem
        self.fields['tipo_error_ingresos_mensuales'].queryset = Errores_agravante.objects.filter(item='ingresos_mensuales')# type: ignore
        self.fields['tipo_error_monto_renegociado'].queryset = Errores_agravante.objects.filter(item='monto_renegociado')# type: ignore

class EvaluacionIngresoDeDatosForm(forms.ModelForm):
    class Meta:
        model = EvaluacionIngresoDeDatos
        fields = [
            'respuesta_actividad',
            'obs_actividad_dice',
            'obs_actividad_debe',
            'observacion_actividad',
            'respuesta_direccion_part',
            'obs_direccion_part_dice',
            'obs_direccion_part_debe',
            'observacion_direccion_part',
            'respuesta_universidad',
            'obs_universidad_dice',
            'obs_universidad_debe',
            'observacion_universidad',
            'respuesta_fecha_in_empleo',
            'obs_fecha_in_empleo_dice',
            'obs_fecha_in_empleo_debe',
            'observacion_fecha_in_empleo',
            'respuesta_nivel_educa',
            'obs_nivel_educa_dice',
            'obs_nivel_educa_debe',
            'observacion_nivel_educa',
            'respuesta_nacionalidad',
            'obs_nacionalidad_dice',
            'obs_nacionalidad_debe',
            'observacion_nacionalidad',
            'respuesta_tipo_contrato',
            'obs_tipo_contrato_dice',
            'obs_tipo_contrato_debe',
            'observacion_tipo_contrato',
            'respuesta_tipo_renta',
            'obs_tipo_renta_dice',
            'obs_tipo_renta_debe',
            'observacion_tipo_renta',
            'respuesta_carrera_semestre',
            'obs_carrera_semestre_dice',
            'obs_carrera_semestre_debe',
            'observacion_carrera_semestre',
            'respuesta_profesion',
            'obs_profesion_dice',
            'obs_profesion_debe',
            'observacion_profesion',
            'respuesta_estado_civil',
            'obs_estado_civil_dice',
            'obs_estado_civil_debe',
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