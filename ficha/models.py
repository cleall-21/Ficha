from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='static/img', default='default.jpg')
    ci = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.user.username
    
ITEMS = [
    ('verificacion_laboral', 'Verificación Laboral'),
    ('estado_situacion', 'Estado de Situación'),
    ('acreditacion_ingresos', 'Acreditación de Ingresos'),
    ('error_atribuciones', 'Atribuciones'),
    ('contribucion_garantia', 'Constitución Garantías y/o Aval'),
    ('condiciones_aprobacion', 'Condiciones Aprobación'),
    ('cambio_evaAT', 'Cambio Evaluación AT'),
    ('ingresos_mensuales', 'Ingresos Mensuales'),
    ('monto_renegociado', 'Monto a Reestructurar Renegociado Corto Plazo y/o Largo Plazo'),
    # Aqui se puede agregar más ítems para los demas formularios
]
class Errores_agravante(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_error = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=5, decimal_places=1)
    item = models.CharField(max_length=50, choices=ITEMS)
    def __str__(self):
        return f"{self.tipo_error}"

RESPUESTAS = [
    ('Sin Error','sin error'),
    ('Error','error'),
    ('N/A','n/a'),
]
TIPOS = [
    ('Prospecto','prospecto'),
    ('Nuevo','nuevo'),
    ('Antiguo','antiguo'),
    ('Plus','plus')
]
class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(max_length=10, blank=True, choices=TIPOS)
    fecha = models.DateField()
    nota_final = models.DecimalField(max_digits=5, decimal_places=2)
    clasificacion = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Evaluación {self.id_evaluacion}, Fecha: {self.fecha} - {self.user}"

    def calcular_nota_final(self):
        nota_minima = 5.0  # Valor base máximo

        # Formalidad
        for detalle in self.formalidad.all(): # type: ignore

            notas = detalle.get_notas_agravantes()
            if notas:
                nota_minima = min(nota_minima, *notas)

        # Gestión Otorga
        for detalle in self.gestion_otorga.all():# type: ignore
            notas = detalle.get_notas_agravantes()
            if notas:
                nota_minima = min(nota_minima, *notas)

        # Depuración de Antecedentes
        for detalle in self.depuracion_antecedentes.all():# type: ignore
            notas = detalle.get_notas_agravantes()
            if notas:
                nota_minima = min(nota_minima, *notas)

        # Ingreso de Datos no tiene errores agravantes por ahora
        self.nota_final = nota_minima
        self.clasificacion = self.obtener_clasificacion(nota_minima)
        self.save()

    def obtener_clasificacion(self, nota):
        if nota < 2:
            return "Deficiente"
        elif nota < 3:
            return "Insuficiente"
        elif nota < 4:
            return "Regular"
        elif nota < 4.5:
            return "Aceptable"
        elif nota < 5:
            return "Destacado"
        else:
            return "Excelente"


class EvaluacionFormalidad(models.Model):
    id_evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='formalidad')
    # Verificación Laboral
    respuesta_verificacion_laboral = models.CharField(max_length=10, choices=RESPUESTAS)
    tipo_error_verificacion_laboral = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_verificacion_laboral'
    )
    observacion_verificacion = models.CharField(max_length=100, blank=True)
    # Estado de Situación
    respuesta_estado_situacion = models.CharField(max_length=10, choices=RESPUESTAS)
    tipo_error_estado_situacion = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_estado_situacion'
    )
    observacion_estado = models.CharField(max_length=100, blank=True)
    # Acreditación de Ingresos
    respuesta_acreditacion_ingresos = models.CharField(max_length=10, choices=RESPUESTAS)
    tipo_error_acreditacion_ingresos = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_acreditacion_ingresos'
    )
    observacion_acreditacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Evaluación Formalidad - {self.id_evaluacion}"

    def get_notas_agravantes(self):
        notas = []
        if self.tipo_error_verificacion_laboral:
            notas.append(self.tipo_error_verificacion_laboral.nota)
        if self.tipo_error_estado_situacion:
            notas.append(self.tipo_error_estado_situacion.nota)
        if self.tipo_error_acreditacion_ingresos:
            notas.append(self.tipo_error_acreditacion_ingresos.nota)
        return notas
class EvaluacionGestionOtorga(models.Model):
    id_evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='gestion_otorga')
    # Atribuciones
    respuesta_atribuciones = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_atribuciones = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_atribuciones'
    )
    observaciones_revision_credito = models.CharField(max_length=100, blank=True)
    # Contribución Garantías y/o Aval
    respuesta_contribucion_garantia = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_contribucion_garantia = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_contribucion_garantia'
    )
    observaciones_contribucion_garantia = models.CharField(max_length=100, blank=True)
    # Condiciones de Aprobación
    respuesta_condiciones_aprobacion = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_condiciones_aprobacion = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_condiciones_aprobacion'
    )
    observacion_condicion_aprob = models.CharField(max_length=100, blank=True)
    # Cambio Resultado Evaluación Automática
    respuesta_cambio_evaAT = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_cambio_evaAT = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_cambio_evaAT'
    )
    observacion_cambioEva = models.CharField(max_length=100, blank=True)
    # Deudas Vinculadas
    respuesta_deudas_vinculadas = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_res_deuda_vincu = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Gestión Otorgamiento de evaluación {self.id_evaluacion}"

    def get_notas_agravantes(self):
        notas = []
        if self.tipo_error_condiciones_aprobacion:
            notas.append(self.tipo_error_condiciones_aprobacion.nota)
        if self.tipo_error_cambio_evaAT:
            notas.append(self.tipo_error_cambio_evaAT.nota)
        return notas
class EvaluacionDepuracionAntecedentes(models.Model):
    id_evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='depuracion_antecedentes')
    # Ingresos Mensuales
    respuesta_ingresos_mensuales = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_ingresos_mensuales = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingresos_mensuales'
    )
    obs_ingresos_mensuales_dice = models.CharField(max_length=50, blank=True)
    obs_ingresos_mensuales_debe = models.CharField(max_length=50, blank=True)
    observacion_ingresos_mensuales = models.CharField(max_length=200, blank=True)
    # Activo
    respuesta_activo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_activo_dice = models.CharField(max_length=50, blank=True)
    obs_activo_debe = models.CharField(max_length=50, blank=True)
    observacion_activo = models.CharField(max_length=100, blank=True)
    # Dividendo BCH (actual y sin cursar) o Gasto Vivienda
    respuesta_dividendo_BCH = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_dividendo_BCH_dice = models.CharField(max_length=50, blank=True)
    obs_dividendo_BCH_debe = models.CharField(max_length=50, blank=True)
    observacion_dividendo_BCH = models.CharField(max_length=100, blank=True)
    # Arriendos Pagados
    respuesta_arriendos = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_arriendos_dice = models.CharField(max_length=50, blank=True)
    obs_arriendos_debe = models.CharField(max_length=50, blank=True)
    observacion_arriendos = models.CharField(max_length=100, blank=True)
    # Cuota Préstamo Empleador y/o CCAF
    respuesta_cuota_prestamo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_cuota_prestamo_dice = models.CharField(max_length=50, blank=True)
    obs_cuota_prestamo_debe = models.CharField(max_length=50, blank=True)
    observacion_cuota_prestamo = models.CharField(max_length=100, blank=True)
    # Otros Egresos
    respuesta_otros_egre = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_otros_egre_dice = models.CharField(max_length=50, blank=True)
    obs_otros_egre_debe = models.CharField(max_length=50, blank=True)
    observacion_otros_egre = models.CharField(max_length=100, blank=True)
    # Monto a Reestructurar Renegociado Corto Plazo y Largo Plazo
    respuesta_renegociado = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_monto_renegociado = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='monto_renegociado'
    )
    obs_renegociado_dice = models.CharField(max_length=50, blank=True)
    obs_renegociado_debe = models.CharField(max_length=50, blank=True)
    observacion_renegociado = models.CharField(max_length=100, blank=True)
    # Cuota Banco CP (Compra Cartera)
    respuesta_cuota_cp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_cuota_cp_dice = models.CharField(max_length=50, blank=True)
    obs_cuota_cp_debe = models.CharField(max_length=50, blank=True)
    observacion_cuota_cp = models.CharField(max_length=100, blank=True)
    # Cuota Compra OOII (Compra Cartera)
    respuesta_cuota_ooii = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_cuota_ooii_dice = models.CharField(max_length=50, blank=True)
    obs_cuota_ooii_debe = models.CharField(max_length=50, blank=True)
    observacion_cuota_ooii = models.CharField(max_length=100, blank=True)
    # Monto Compra Banco LP (Compra Cartera)
    respuesta_monto_compra_lp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_monto_compra_lp_dice = models.CharField(max_length=50, blank=True)
    obs_monto_compra_lp_debe = models.CharField(max_length=50, blank=True)
    observacion_monto_compra_lp = models.CharField(max_length=100, blank=True)
    # Monto Compra Banco CP (Compra Cartera)
    respuesta_monto_compra_cp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_monto_compra_cp_dice = models.CharField(max_length=50, blank=True)
    obs_monto_compra_cp_debe = models.CharField(max_length=50, blank=True)
    observacion_monto_compra_cp = models.CharField(max_length=100, blank=True)
    # Monto Compra OOII (Compra Cartera)
    respuesta_monto_compra_ooii = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_monto_compra_ooii_dice = models.CharField(max_length=50, blank=True)
    obs_monto_compra_ooii_debe = models.CharField(max_length=50, blank=True)
    observacion_monto_compra_ooii = models.CharField(max_length=100, blank=True)
    # Monto Compra SBIF (Compra Cartera)
    respuesta_monto_compra_sbif = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_monto_compra_sbif_dice = models.CharField(max_length=50, blank=True)
    obs_monto_compra_sbif_debe = models.CharField(max_length=50, blank=True)
    observacion_monto_compra_sbif = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Depuración de Antecedentes de evaluación {self.id_evaluacion}"

    def get_notas_agravantes(self):
        notas = []
        if self.tipo_error_ingresos_mensuales:
            notas.append(self.tipo_error_ingresos_mensuales.nota)
        if self.tipo_error_monto_renegociado:
            notas.append(self.tipo_error_monto_renegociado.nota)
        return notas
class EvaluacionIngresoDeDatos(models.Model):
    id_evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='ingreso_datos')
    # Actividad
    respuesta_actividad = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_actividad_dice = models.CharField(max_length=50, blank=True)
    obs_actividad_debe = models.CharField(max_length=50, blank=True)
    observacion_actividad = models.CharField(max_length=100,blank=True)
    # Dirección Particular
    respuesta_direccion_part = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_direccion_part_dice = models.CharField(max_length=50, blank=True)
    obs_direccion_part_debe = models.CharField(max_length=50, blank=True)
    observacion_direccion_part = models.CharField(max_length=100,blank=True)
  # Universidad
    respuesta_universidad = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_universidad_dice = models.CharField(max_length=50, blank=True)
    obs_universidad_debe = models.CharField(max_length=50, blank=True)
    observacion_universidad = models.CharField(max_length=100,blank=True)
  # Fecha de Ingreso Empleo
    respuesta_fecha_in_empleo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_fecha_in_empleo_dice = models.CharField(max_length=50, blank=True)
    obs_fecha_in_empleo_debe = models.CharField(max_length=50, blank=True)
    observacion_fecha_in_empleo = models.CharField(max_length=100,blank=True)
  # Nivel Educacional
    respuesta_nivel_educa = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_nivel_educa_dice = models.CharField(max_length=50, blank=True)
    obs_nivel_educa_debe = models.CharField(max_length=50, blank=True)
    observacion_nivel_educa = models.CharField(max_length=100,blank=True)
  # Nacionalidad
    respuesta_nacionalidad = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_nacionalidad_dice = models.CharField(max_length=50, blank=True)
    obs_nacionalidad_debe = models.CharField(max_length=50, blank=True)
    observacion_nacionalidad = models.CharField(max_length=100,blank=True)
  # Tipo de Contrato
    respuesta_tipo_contrato = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_tipo_contrato_dice = models.CharField(max_length=50, blank=True)
    obs_tipo_contrato_debe = models.CharField(max_length=50, blank=True)
    observacion_tipo_contrato = models.CharField(max_length=100,blank=True)
  # Tipo de Renta
    respuesta_tipo_renta = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_tipo_renta_dice = models.CharField(max_length=50, blank=True)
    obs_tipo_renta_debe = models.CharField(max_length=50, blank=True)
    observacion_tipo_renta = models.CharField(max_length=100,blank=True)
  # Carrera/Semestre
    respuesta_carrera_semestre = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_carrera_semestre_dice = models.CharField(max_length=50, blank=True)
    obs_carrera_semestre_debe = models.CharField(max_length=50, blank=True)
    observacion_carrera_semestre = models.CharField(max_length=100,blank=True)
  # Profesión
    respuesta_profesion = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_profesion_dice = models.CharField(max_length=50, blank=True)
    obs_profesion_debe = models.CharField(max_length=50, blank=True)
    observacion_profesion = models.CharField(max_length=100,blank=True)
  # Estado Civil
    respuesta_estado_civil = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    obs_estado_civil_dice = models.CharField(max_length=50, blank=True)
    obs_estado_civil_debe = models.CharField(max_length=50, blank=True)
    observacion_estado_civil = models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return f"Ingreso de Datos de evaluación {self.id_evaluacion}"
class Registro_materialidad(models.Model):
    id_registro = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    dv = models.CharField(max_length=1)
    log_fecha_registro = models.CharField(max_length=20)
    login_creador = models.CharField(max_length=100)
    nombre_ejecutivo = models.CharField(max_length=100)
    rut_ejecutivo = models.CharField(max_length=12)
    oficina_ejecutivo = models.CharField(max_length=100)
    cui = models.CharField(max_length=20)
    etapa_venta_actual = models.CharField(max_length=100)
    inconsistencia = models.CharField(max_length=100)
    max_prod_rgo = models.CharField(max_length=100)
    monto_oferta = models.CharField(max_length=100)
    proceso_credito = models.CharField(max_length=100)
    pauta_evaluacion = models.CharField(max_length=100)
    ano_mes = models.CharField(max_length=6)
    canal = models.CharField(max_length=100)
    prod_eval = models.CharField(max_length=100)
    mes_nombre = models.CharField(max_length=20)
    estado = models.CharField(max_length=100)
    codigo_suc = models.CharField(max_length=10)
    nombre_suc = models.CharField(max_length=100)
    aprobador = models.CharField(max_length=100)
    id_oportunidad = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.id_registro}"

#class reporte(models.Model):
    #id_reporte = models.AutoField(primary_key=True)
    #name_reporte = models.CharField(max_length=50)

    #def __str__(self):
        #return f{N° Reporte{self.id_reporte}, {self.name_reporte}}""
