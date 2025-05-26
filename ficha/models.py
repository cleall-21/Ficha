from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MaxValueValidator
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
    ('constitucion_garantia', 'Constitución Garantías y/o Aval'),
    ('condiciones_aprobacion', 'Condiciones Aprobación'),
    ('cambio_evaAT', 'Cambio Evaluación AT'),
    ('ingresos_mensuales', 'Ingresos Mensuales'),
    ('monto_renegociado', 'Monto a Reestructurar Renegociado Corto Plazo y/o Largo Plazo'),
    # Aqui se puede agregar más tipos de agravantes segun el parametro
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
    # Campos traídos desde Formulario 1
    rut_cliente = models.CharField(max_length=12,default="Rut no registrado") # AGREGAR RUT DEL EJECUTIVO Y ADEMAS CAMBIAR NOMBRE DE RUT A RUT_CLIENTE PARA EVITAR CONFUSIONES DE USERS
    nombre_ejec = models.CharField(max_length=100,default="Nombre no encontrado")
    login_ejecutivo = models.CharField(max_length=50,default="Login no encontrado")
    rut_ejec = models.CharField(max_length=12,default="Rut no registrado") 
    sucursal = models.CharField(max_length=100,default="Sucursal no encontrada")
    codigo_sucursal = models.IntegerField(validators= [MaxValueValidator(999999999999999)],default=0)
    producto = models.CharField(max_length=100,default="Producto no encontrado")
    monto_solicitado =  models.CharField(max_length=20,default="Monto no encontrado") 
    proceso_credito = models.CharField(max_length=50,default="Tipo de credito no encontrado") 
    # Campos existentes
    tipo_cliente = models.CharField(max_length=10, blank=True, choices=TIPOS)
    fecha = models.DateField()
    nota_final = models.DecimalField(max_digits=5, decimal_places=2)
    clasificacion = models.CharField(max_length=15)
    cantidad_errores = models.PositiveIntegerField(default=0) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Evaluación {self.id_evaluacion}, Fecha: {self.fecha} - {self.user}"

    def calcular_nota_final(self):
        nota_minima = Decimal('5.0')
        errores_agregados = False

        # Formalidad
        for detalle in self.formalidad.all():  # type: ignore
            notas = detalle.get_notas_agravantes()
            if notas:
                errores_agregados = True
                nota_minima = min(nota_minima, *notas)

        # Gestión Otorga
        for detalle in self.gestion_otorga.all():  # type: ignore
            notas = detalle.get_notas_agravantes()
            if notas:
                errores_agregados = True
                nota_minima = min(nota_minima, *notas)

        # Depuración de Antecedentes
        for detalle in self.depuracion_antecedentes.all():  # type: ignore
            notas = detalle.get_notas_agravantes()
            if notas:
                errores_agregados = True
                nota_minima = min(nota_minima, *notas)

        self.cantidad_errores = self.contar_errores_totales()

        # Si no hay errores agravantes, usar nota por cantidad de errores
        if not errores_agregados:
            nota_minima = self.obtener_nota_por_errores(self.cantidad_errores)
        else:
            # Ajustar nota mínima según cantidad de errores
            if self.cantidad_errores > 5:
                nota_minima = Decimal('1')
            elif self.cantidad_errores == 5:
                nota_minima = max(Decimal('1'), nota_minima - Decimal('0.5'))
            elif self.cantidad_errores in [3, 4]:
                nota_minima = max(Decimal('1'), nota_minima )

        self.nota_final = nota_minima
        self.clasificacion = self.obtener_clasificacion(nota_minima)
        self.save()

    def contar_errores_totales(self):
        total_errores = 0
        
        for detalle in self.formalidad.all():  # type: ignore
            total_errores += detalle.contar_errores()

        for detalle in self.gestion_otorga.all():  # type: ignore
            total_errores += detalle.contar_errores()

        for detalle in self.depuracion_antecedentes.all():  # type: ignore
            total_errores += detalle.contar_errores()

        for detalle in self.ingreso_datos.all():  # type: ignore
            total_errores += detalle.contar_errores()

        return total_errores

    def obtener_nota_por_errores(self, cantidad_errores):
        if cantidad_errores == 0:
            return 5
        elif cantidad_errores <=2:
            return 4.5 
        elif cantidad_errores == 3:
            return 3.5
        elif cantidad_errores == 4:
            return 3
        elif cantidad_errores == 5:
            return 2.5
        elif cantidad_errores > 5:
            return 1

    def obtener_clasificacion(self, nota):
        if nota < 2.5:
            return "Deficiente"
        elif nota < 3:
            return "Insuficiente"
        elif nota < 3.5:
            return "Regular"
        elif nota < 4:
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
    observacion_verificacion = models.CharField(max_length=350, blank=True)
    # Estado de Situación
    respuesta_estado_situacion = models.CharField(max_length=10, choices=RESPUESTAS)
    tipo_error_estado_situacion = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_estado_situacion'
    )
    observacion_estado = models.CharField(max_length=350, blank=True)
    # Acreditación de Ingresos
    respuesta_acreditacion_ingresos = models.CharField(max_length=10, choices=RESPUESTAS)
    tipo_error_acreditacion_ingresos = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_acreditacion_ingresos'
    )
    observacion_acreditacion = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return f"Evaluación Formalidad - {self.id_evaluacion}"
    def contar_errores(self):
        errores = 0
        respuestas = [
            self.respuesta_verificacion_laboral,
            self.respuesta_estado_situacion,
            self.respuesta_acreditacion_ingresos,
        ]
        errores = sum(1 for r in respuestas if r == 'Error')
        return errores

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
    observaciones_atribuciones = models.CharField(max_length=350, blank=True)
    respuesta_constitucion_garantia = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_constitucion_garantia = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_constitucion_garantia'
    )
    observaciones_constitucion_garantia = models.CharField(max_length=350, blank=True)
    # Condiciones de Aprobación
    respuesta_condiciones_aprobacion = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_condiciones_aprobacion = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_condiciones_aprobacion'
    )
    observacion_condicion_aprob = models.CharField(max_length=350, blank=True)
    # Cambio Resultado Evaluación Automática
    respuesta_cambio_evaAT = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_cambio_evaAT = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errores_cambio_evaAT'
    )
    observacion_cambioEva = models.CharField(max_length=350, blank=True)
    # Deudas Vinculadas
    respuesta_deudas_vinculadas = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_res_deuda_vincu = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return f"Gestión Otorgamiento de evaluación {self.id_evaluacion}"
    def contar_errores(self):
        errores = 0
        respuestas = [
            self.respuesta_atribuciones,
            self.respuesta_constitucion_garantia,
            self.respuesta_condiciones_aprobacion,
            self.respuesta_cambio_evaAT,
            self.respuesta_deudas_vinculadas,
        ]
        errores = sum(1 for r in respuestas if r == 'Error')
        return errores
    
    def get_notas_agravantes(self):
        notas = []
        if self.tipo_error_atribuciones:
            notas.append(self.tipo_error_atribuciones.nota)
        if self.tipo_error_constitucion_garantia:
            notas.append(self.tipo_error_constitucion_garantia.nota)
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
    observacion_ingresos_mensuales = models.CharField(max_length=200, blank=True)
    # Activo
    respuesta_activo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_activo = models.CharField(max_length=350, blank=True)
    # Dividendo BCH (actual y sin cursar) o Gasto Vivienda
    respuesta_dividendo_BCH = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_dividendo_BCH = models.CharField(max_length=350, blank=True)
    # Arriendos Pagados
    respuesta_arriendos = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_arriendos = models.CharField(max_length=350, blank=True)
    # Cuota Préstamo Empleador y/o CCAF
    respuesta_cuota_prestamo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_cuota_prestamo = models.CharField(max_length=350, blank=True)
    # Monto a Reestructurar Renegociado Corto Plazo y Largo Plazo
    respuesta_renegociado = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    tipo_error_monto_renegociado = models.ForeignKey(
        Errores_agravante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='monto_renegociado'
    )
    observacion_renegociado = models.CharField(max_length=350, blank=True)
    # Otros Egresos
    respuesta_otros_egre = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_otros_egre = models.CharField(max_length=350, blank=True)
    # opcion para reducir tiempo de desarrollo
    corresponde_compra_cartera = models.BooleanField(default=False, verbose_name="¿Corresponde compra cartera?")
    # Cuota Banco CP (Compra Cartera)
    respuesta_cuota_cp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_cuota_cp = models.CharField(max_length=350, blank=True)
    # Cuota Compra OOII (Compra Cartera)
    respuesta_cuota_ooii = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_cuota_ooii = models.CharField(max_length=350, blank=True)
    # Monto Compra Banco LP (Compra Cartera)
    respuesta_monto_compra_lp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_monto_compra_lp = models.CharField(max_length=350, blank=True)
    # Monto Compra Banco CP (Compra Cartera)
    respuesta_monto_compra_cp = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_monto_compra_cp = models.CharField(max_length=350, blank=True)
    # Monto Compra OOII (Compra Cartera)
    respuesta_monto_compra_ooii = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_monto_compra_ooii = models.CharField(max_length=350, blank=True)
    # Monto Compra SBIF (Compra Cartera)
    respuesta_monto_compra_sbif = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_monto_compra_sbif = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return f"Depuración de Antecedentes de evaluación {self.id_evaluacion}"
    def contar_errores(self):
        errores = 0
        respuestas = [
            self.respuesta_ingresos_mensuales,
            self.respuesta_activo,
            self.respuesta_dividendo_BCH,
            self.respuesta_arriendos,
            self.respuesta_cuota_prestamo,
            self.respuesta_otros_egre,
            self.respuesta_renegociado,
            self.respuesta_cuota_cp,
            self.respuesta_cuota_ooii,
            self.respuesta_monto_compra_lp,
            self.respuesta_monto_compra_cp,
            self.respuesta_monto_compra_ooii,
            self.respuesta_monto_compra_sbif,
        ]
        errores = sum(1 for r in respuestas if r == 'Error')
        return errores
    
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
    observacion_actividad = models.CharField(max_length=350,blank=True)
    # Dirección Particular
    respuesta_direccion_part = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_direccion_part = models.CharField(max_length=350,blank=True)
  # Universidad
    respuesta_universidad = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_universidad = models.CharField(max_length=350,blank=True)
  # Fecha de Ingreso Empleo
    respuesta_fecha_in_empleo = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_fecha_in_empleo = models.CharField(max_length=350,blank=True)
  # Nivel Educacional
    respuesta_nivel_educa = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_nivel_educa = models.CharField(max_length=350,blank=True)
  # Nacionalidad
    respuesta_nacionalidad = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_nacionalidad = models.CharField(max_length=350,blank=True)
  # Tipo de Contrato
    respuesta_tipo_contrato = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_tipo_contrato = models.CharField(max_length=350,blank=True)
  # Tipo de Renta
    respuesta_tipo_renta = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_tipo_renta = models.CharField(max_length=350,blank=True)
  # Carrera/Semestre
    respuesta_carrera_semestre = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_carrera_semestre = models.CharField(max_length=350,blank=True)
  # Profesión
    respuesta_profesion = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_profesion = models.CharField(max_length=350,blank=True)
  # Estado Civil
    respuesta_estado_civil = models.CharField(max_length=10, choices=RESPUESTAS, blank=True)
    observacion_estado_civil = models.CharField(max_length=350,blank=True)
    
    def __str__(self):
        return f"Ingreso de Datos de evaluación {self.id_evaluacion}"
    def contar_errores(self):
        respuestas = [
            self.respuesta_actividad,
            self.respuesta_direccion_part,
            self.respuesta_universidad,
            self.respuesta_fecha_in_empleo,
            self.respuesta_nivel_educa,
            self.respuesta_nacionalidad,
            self.respuesta_tipo_contrato,
            self.respuesta_tipo_renta,
            self.respuesta_carrera_semestre,
            self.respuesta_profesion,
            self.respuesta_estado_civil,
        ]
        return sum(1 for r in respuestas if r == 'Error')

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
    nombre_suc = models.CharField(max_length=300)
    aprobador = models.CharField(max_length=100)
    id_oportunidad = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.id_registro}"