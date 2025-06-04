from collections import defaultdict

def promedio_a_etiqueta(promedio):
    if promedio < 2.5:
        return 'Deficiente'
    elif promedio < 3:
        return 'Insuficiente'
    elif promedio < 3.5:
        return 'Regular'
    elif promedio < 4:
        return 'Aceptable'
    elif promedio < 5:
        return 'Destacado'
    else:
        return 'Excelente'

def calculo_tabla(evaluacion_queryset):
    resumen = defaultdict(lambda: {
        'Excelente': 0,
        'Destacado': 0,
        'Aceptable': 0,
        'Regular': 0,
        'Insuficiente': 0,
        'Deficiente': 0,
        'Total_Calificaciones': 0,
        'Suma_Notas': 0.0,
        'Calificacion_Final': ''
    })

    for ev in evaluacion_queryset:
        nombre = ev.nombre_ejec
        clasificacion = ev.clasificacion
        nota = float(ev.nota_final)

        if clasificacion in resumen[nombre]:
            resumen[nombre][clasificacion] += 1 # type: ignore
        else:
            resumen[nombre][clasificacion] = 1


        resumen[nombre]['Total_Calificaciones'] += 1 # type: ignore
        resumen[nombre]['Suma_Notas'] += nota # type: ignore

    for nombre, datos in resumen.items():
        total = datos['Total_Calificaciones']
        suma = datos['Suma_Notas']
        promedio = suma / total if total > 0 else 0 # type: ignore
        datos['Calificacion_Final'] = promedio_a_etiqueta(promedio)

    return dict(resumen)

def extraer_observaciones(evaluacion):
    observaciones = []
    modelos = [
        ('Formalidad', evaluacion.formalidad.all(), {
            'observacion_verificacion': 'Verificación Laboral',
            'observacion_estado': 'Estado de Situación',
            'observacion_acreditacion': 'Acreditación de Ingresos',
        }),
        ('Gestión Otorga', evaluacion.gestion_otorga.all(), {
            'observaciones_atribuciones': 'Atribuciones',
            'observaciones_constitucion_garantia': 'Constitución Garantía',
            'observacion_condicion_aprob': 'Condiciones de Aprobación',
            'observacion_cambioEva': 'Cambio Evaluación Automática',
            'observacion_res_deuda_vincu': 'Deudas Vinculadas',
        }),
        ('Depuración Antecedentes', evaluacion.depuracion_antecedentes.all(), {
            'observacion_ingresos_mensuales': 'Ingresos Mensuales',
            'observacion_activo': 'Activo',
            'observacion_dividendo_BCH': 'Dividendo BCH',
            'observacion_arriendos': 'Arriendos Pagados',
            'observacion_cuota_prestamo': 'Cuota Préstamo',
            'observacion_renegociado': 'Monto Renegociado',
            'observacion_otros_egre': 'Otros Egresos',
            'observacion_cuota_cp': 'Cuota CP',
            'observacion_cuota_ooii': 'Cuota OOII',
            'observacion_monto_compra_lp': 'Monto Compra LP',
            'observacion_monto_compra_cp': 'Monto Compra CP',
            'observacion_monto_compra_ooii': 'Monto Compra OOII',
            'observacion_monto_compra_sbif': 'Monto Compra SBIF',
        }),
        ('Ingreso de Datos', evaluacion.ingreso_datos.all(), {
            'observacion_actividad': 'Actividad',
            'observacion_direccion_part': 'Dirección Particular',
            'observacion_universidad': 'Universidad',
            'observacion_fecha_in_empleo': 'Fecha Ingreso Empleo',
            'observacion_nivel_educa': 'Nivel Educacional',
            'observacion_nacionalidad': 'Nacionalidad',
            'observacion_tipo_contrato': 'Tipo Contrato',
            'observacion_tipo_renta': 'Tipo Renta',
            'observacion_carrera_semestre': 'Carrera/Semestre',
            'observacion_profesion': 'Profesión',
            'observacion_estado_civil': 'Estado Civil',
        }),
    ]

    for item, queryset, campos in modelos:
        for instancia in queryset:
            for campo, concepto in campos.items():
                valor = getattr(instancia, campo, '')
                if valor:
                    observaciones.append({
                        'rut_cliente': evaluacion.rut_cliente,
                        'producto': evaluacion.producto,
                        'item': item,
                        'concepto': concepto,
                        'observacion': valor,
                        'tipo_cliente': evaluacion.tipo_cliente,
                        'tipo_evaluacion': evaluacion.proceso_credito,
                    })
    return observaciones
def porcentaje_cumplimiento(evaluacion):
    respuesta = []
    modelos = [
        ('Formalidad', evaluacion.formalidad.all(), {
            'respuesta_verificacion_laboral',
            'respuesta_estado_situacion',
            'respuesta_acreditacion_ingresos'
        }),
        ('Gestión Otorga', evaluacion.gestion_otorga.all(),{
            'respuesta_atribuciones',
            'respuesta_constitucion_garantia',
            'respuesta_condiciones_aprobacion',
            'respuesta_cambio_evaAT',
            'respuesta_deudas_vinculadas',
        }),
        ('Depuración Antecedentes', evaluacion.depuracion_antecedentes.all(),{
            'respuesta_ingresos_mensuales',
            'respuesta_activo',
            'respuesta_dividendo_BCH',
            'respuesta_arriendos',
            'respuesta_cuota_prestamo',
            'respuesta_renegociado',
            'respuesta_otros_egre',
            'respuesta_cuota_cp',
            'respuesta_cuota_ooii',
            'respuesta_monto_compra_lp',
            'respuesta_monto_compra_cp',
            'respuesta_monto_compra_ooii',
            'respuesta_monto_compra_sbif',
        }),
        ('Ingreso de Datos', evaluacion.ingreso_datos.all(),{
            'respuesta_actividad',
            'respuesta_direccion_part',
            'respuesta_universidad',
            'respuesta_fecha_in_empleo',
            'respuesta_nivel_educa',
            'respuesta_nacionalidad',
            'respuesta_tipo_contrato',
            'respuesta_tipo_renta',
            'respuesta_carrera_semestre',
            'respuesta_profesion',
            'respuesta_estado_civil',
        })
    ]