# Generated by Django 5.1.7 on 2025-05-27 20:59

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ficha", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Registro_materialidad",
            fields=[
                ("id_registro", models.AutoField(primary_key=True, serialize=False)),
                ("rut", models.CharField(max_length=12)),
                ("dv", models.CharField(max_length=1)),
                ("log_fecha_registro", models.CharField(max_length=20)),
                ("login_creador", models.CharField(max_length=100)),
                ("nombre_ejecutivo", models.CharField(max_length=100)),
                ("rut_ejecutivo", models.CharField(max_length=12)),
                ("oficina_ejecutivo", models.CharField(max_length=100)),
                ("cui", models.CharField(max_length=20)),
                ("etapa_venta_actual", models.CharField(max_length=100)),
                ("inconsistencia", models.CharField(max_length=100)),
                ("max_prod_rgo", models.CharField(max_length=100)),
                ("monto_oferta", models.CharField(max_length=100)),
                ("proceso_credito", models.CharField(max_length=100)),
                ("pauta_evaluacion", models.CharField(max_length=100)),
                ("ano_mes", models.CharField(max_length=6)),
                ("canal", models.CharField(max_length=100)),
                ("prod_eval", models.CharField(max_length=100)),
                ("mes_nombre", models.CharField(max_length=20)),
                ("estado", models.CharField(max_length=100)),
                ("codigo_suc", models.CharField(max_length=10)),
                ("nombre_suc", models.CharField(max_length=300)),
                ("aprobador", models.CharField(max_length=100)),
                ("id_oportunidad", models.CharField(max_length=45)),
            ],
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="evaluacion",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_activo_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_activo_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_arriendos_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_arriendos_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_cp_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_cp_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_ooii_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_ooii_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_prestamo_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_cuota_prestamo_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_dividendo_BCH_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_dividendo_BCH_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_ingresos_mensuales_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_ingresos_mensuales_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_cp_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_cp_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_lp_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_lp_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_ooii_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_ooii_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_sbif_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_monto_compra_sbif_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_otros_egre_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_otros_egre_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_renegociado_debe",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="obs_renegociado_dice",
        ),
        migrations.RemoveField(
            model_name="evaluaciondepuracionantecedentes",
            name="user",
        ),
        migrations.RemoveField(
            model_name="evaluacionformalidad",
            name="evaluacion",
        ),
        migrations.RemoveField(
            model_name="evaluacionformalidad",
            name="user",
        ),
        migrations.RemoveField(
            model_name="evaluaciongestionotorga",
            name="evaluacion",
        ),
        migrations.RemoveField(
            model_name="evaluaciongestionotorga",
            name="observaciones_contribucion_garantia",
        ),
        migrations.RemoveField(
            model_name="evaluaciongestionotorga",
            name="observaciones_revision_credito",
        ),
        migrations.RemoveField(
            model_name="evaluaciongestionotorga",
            name="respuesta_contribucion_garantia",
        ),
        migrations.RemoveField(
            model_name="evaluaciongestionotorga",
            name="user",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="evaluacion",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_actividad_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_actividad_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_carrera_semestre_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_carrera_semestre_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_direccion_part_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_direccion_part_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_estado_civil_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_estado_civil_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_fecha_in_empleo_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_fecha_in_empleo_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_nacionalidad_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_nacionalidad_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_nivel_educa_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_nivel_educa_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_profesion_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_profesion_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_tipo_contrato_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_tipo_contrato_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_tipo_renta_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_tipo_renta_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_universidad_debe",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="obs_universidad_dice",
        ),
        migrations.RemoveField(
            model_name="evaluacioningresodedatos",
            name="user",
        ),
        migrations.AddField(
            model_name="errores_agravante",
            name="item",
            field=models.CharField(
                choices=[
                    ("verificacion_laboral", "Verificación Laboral"),
                    ("estado_situacion", "Estado de Situación"),
                    ("acreditacion_ingresos", "Acreditación de Ingresos"),
                    ("error_atribuciones", "Atribuciones"),
                    ("constitucion_garantia", "Constitución Garantías y/o Aval"),
                    ("condiciones_aprobacion", "Condiciones Aprobación"),
                    ("cambio_evaAT", "Cambio Evaluación AT"),
                    ("ingresos_mensuales", "Ingresos Mensuales"),
                    (
                        "monto_renegociado",
                        "Monto a Reestructurar Renegociado Corto Plazo y/o Largo Plazo",
                    ),
                ],
                default=1,
                max_length=50,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="cantidad_errores",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="codigo_sucursal",
            field=models.IntegerField(
                default=0,
                validators=[django.core.validators.MaxValueValidator(999999999999999)],
            ),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="login_ejecutivo",
            field=models.CharField(default="Login no encontrado", max_length=50),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="monto_solicitado",
            field=models.CharField(default="Monto no encontrado", max_length=20),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="nombre_ejec",
            field=models.CharField(default="Nombre no encontrado", max_length=100),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="proceso_credito",
            field=models.CharField(
                default="Tipo de credito no encontrado", max_length=50
            ),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="producto",
            field=models.CharField(default="Producto no encontrado", max_length=100),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="rut_cliente",
            field=models.CharField(default="Rut no registrado", max_length=12),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="rut_ejec",
            field=models.CharField(default="Rut no registrado", max_length=12),
        ),
        migrations.AddField(
            model_name="evaluacion",
            name="sucursal",
            field=models.CharField(default="Sucursal no encontrada", max_length=100),
        ),
        migrations.AddField(
            model_name="evaluaciondepuracionantecedentes",
            name="corresponde_compra_cartera",
            field=models.BooleanField(
                default=False, verbose_name="¿Corresponde compra cartera?"
            ),
        ),
        migrations.AddField(
            model_name="evaluaciondepuracionantecedentes",
            name="id_evaluacion",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="depuracion_antecedentes",
                to="ficha.evaluacion",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="evaluaciondepuracionantecedentes",
            name="tipo_error_ingresos_mensuales",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ingresos_mensuales",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AddField(
            model_name="evaluaciondepuracionantecedentes",
            name="tipo_error_monto_renegociado",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="monto_renegociado",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AddField(
            model_name="evaluacionformalidad",
            name="id_evaluacion",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="formalidad",
                to="ficha.evaluacion",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="id_evaluacion",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gestion_otorga",
                to="ficha.evaluacion",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="observaciones_atribuciones",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="observaciones_constitucion_garantia",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="respuesta_constitucion_garantia",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="tipo_error_atribuciones",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_atribuciones",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AddField(
            model_name="evaluaciongestionotorga",
            name="tipo_error_constitucion_garantia",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_constitucion_garantia",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AddField(
            model_name="evaluacioningresodedatos",
            name="id_evaluacion",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingreso_datos",
                to="ficha.evaluacion",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="evaluacion",
            name="clasificacion",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_activo",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_arriendos",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_cuota_cp",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_cuota_ooii",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_cuota_prestamo",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_dividendo_BCH",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_monto_compra_cp",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_monto_compra_lp",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_monto_compra_ooii",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_monto_compra_sbif",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_otros_egre",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="observacion_renegociado",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_activo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_arriendos",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_cuota_cp",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_cuota_ooii",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_cuota_prestamo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_dividendo_BCH",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_ingresos_mensuales",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_monto_compra_cp",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_monto_compra_lp",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_monto_compra_ooii",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_monto_compra_sbif",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_otros_egre",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciondepuracionantecedentes",
            name="respuesta_renegociado",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="observacion_acreditacion",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="observacion_estado",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="observacion_verificacion",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="respuesta_acreditacion_ingresos",
            field=models.CharField(
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="respuesta_estado_situacion",
            field=models.CharField(
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="tipo_error_acreditacion_ingresos",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_acreditacion_ingresos",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="tipo_error_estado_situacion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_estado_situacion",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AlterField(
            model_name="evaluacionformalidad",
            name="tipo_error_verificacion_laboral",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_verificacion_laboral",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="observacion_cambioEva",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="observacion_condicion_aprob",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="observacion_res_deuda_vincu",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="respuesta_atribuciones",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="respuesta_cambio_evaAT",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="respuesta_condiciones_aprobacion",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="respuesta_deudas_vinculadas",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="tipo_error_cambio_evaAT",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_cambio_evaAT",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AlterField(
            model_name="evaluaciongestionotorga",
            name="tipo_error_condiciones_aprobacion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="errores_condiciones_aprobacion",
                to="ficha.errores_agravante",
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_actividad",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_carrera_semestre",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_direccion_part",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_estado_civil",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_fecha_in_empleo",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_nacionalidad",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_nivel_educa",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_profesion",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_tipo_contrato",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_tipo_renta",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="observacion_universidad",
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_actividad",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_carrera_semestre",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_direccion_part",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_estado_civil",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_fecha_in_empleo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_nacionalidad",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_nivel_educa",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_profesion",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_tipo_contrato",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_tipo_renta",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="evaluacioningresodedatos",
            name="respuesta_universidad",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sin Error", "sin error"),
                    ("Error", "error"),
                    ("N/A", "n/a"),
                ],
                max_length=10,
            ),
        ),
    ]
