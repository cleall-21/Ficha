# Generated by Django 5.1.7 on 2025-05-07 18:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Errores_agravante",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("tipo_error", models.CharField(max_length=100)),
                ("nota", models.DecimalField(decimal_places=1, max_digits=5)),
            ],
        ),
        
        migrations.CreateModel(
            name="Evaluacion",
            fields=[
                ("id_evaluacion", models.AutoField(primary_key=True, serialize=False)),
                (
                    "tipo_cliente",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Prospecto", "prospecto"),
                            ("Nuevo", "nuevo"),
                            ("Antiguo", "antiguo"),
                            ("Plus", "plus"),
                        ],
                        max_length=10,
                    ),
                ),
                ("fecha", models.DateField()),
                ("nota_final", models.DecimalField(decimal_places=2, max_digits=5)),
                ("clasificacion", models.CharField(max_length=50)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvaluacionDepuracionAntecedentes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "respuesta_ingresos_mensuales",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_ingresos_mensuales_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_ingresos_mensuales_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_ingresos_mensuales",
                    models.CharField(blank=True, max_length=200),
                ),
                (
                    "respuesta_activo",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_activo_dice", models.CharField(blank=True, max_length=50)),
                ("obs_activo_debe", models.CharField(blank=True, max_length=50)),
                ("observacion_activo", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_dividendo_BCH",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_dividendo_BCH_dice", models.CharField(blank=True, max_length=50)),
                ("obs_dividendo_BCH_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_dividendo_BCH",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_arriendos",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_arriendos_dice", models.CharField(blank=True, max_length=50)),
                ("obs_arriendos_debe", models.CharField(blank=True, max_length=50)),
                ("observacion_arriendos", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_cuota_prestamo",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_cuota_prestamo_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_cuota_prestamo_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_cuota_prestamo",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_otros_egre",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_otros_egre_dice", models.CharField(blank=True, max_length=50)),
                ("obs_otros_egre_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_otros_egre",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_renegociado",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_renegociado_dice", models.CharField(blank=True, max_length=50)),
                ("obs_renegociado_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_renegociado",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_cuota_cp",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_cuota_cp_dice", models.CharField(blank=True, max_length=50)),
                ("obs_cuota_cp_debe", models.CharField(blank=True, max_length=50)),
                ("observacion_cuota_cp", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_cuota_ooii",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_cuota_ooii_dice", models.CharField(blank=True, max_length=50)),
                ("obs_cuota_ooii_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_cuota_ooii",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_monto_compra_lp",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_monto_compra_lp_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_monto_compra_lp_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_monto_compra_lp",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_monto_compra_cp",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_monto_compra_cp_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_monto_compra_cp_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_monto_compra_cp",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_monto_compra_ooii",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_monto_compra_ooii_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_monto_compra_ooii_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_monto_compra_ooii",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_monto_compra_sbif",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_monto_compra_sbif_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_monto_compra_sbif_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_monto_compra_sbif",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "evaluacion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ficha.evaluacion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvaluacionFormalidad",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "respuesta_verificacion_laboral",
                    models.CharField(
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "tipo_error_verificacion_laboral",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_verificacion",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_estado_situacion",
                    models.CharField(
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "tipo_error_estado_situacion",
                    models.CharField(blank=True, max_length=50),
                ),
                ("observacion_estado", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_acreditacion_ingresos",
                    models.CharField(
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "tipo_error_acreditacion_ingresos",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_acreditacion",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "evaluacion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ficha.evaluacion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvaluacionGestionOtorga",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "respuesta_atribuciones",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "observaciones_revision_credito",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_contribucion_garantia",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "observaciones_contribucion_garantia",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_condiciones_aprobacion",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "tipo_error_condiciones_aprobacion",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_condicion_aprob",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_cambio_evaAT",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "tipo_error_cambio_evaAT",
                    models.CharField(blank=True, max_length=50),
                ),
                ("observacion_cambioEva", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_deudas_vinculadas",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "observacion_res_deuda_vincu",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "evaluacion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ficha.evaluacion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvaluacionIngresoDeDatos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "respuesta_actividad",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_actividad_dice", models.CharField(blank=True, max_length=50)),
                ("obs_actividad_debe", models.CharField(blank=True, max_length=50)),
                ("observacion_actividad", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_direccion_part",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_direccion_part_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_direccion_part_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_direccion_part",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_universidad",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_universidad_dice", models.CharField(blank=True, max_length=50)),
                ("obs_universidad_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_universidad",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_fecha_in_empleo",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_fecha_in_empleo_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_fecha_in_empleo_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_fecha_in_empleo",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_nivel_educa",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_nivel_educa_dice", models.CharField(blank=True, max_length=50)),
                ("obs_nivel_educa_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_nivel_educa",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_nacionalidad",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_nacionalidad_dice", models.CharField(blank=True, max_length=50)),
                ("obs_nacionalidad_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_nacionalidad",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_tipo_contrato",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_tipo_contrato_dice", models.CharField(blank=True, max_length=50)),
                ("obs_tipo_contrato_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_tipo_contrato",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_tipo_renta",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_tipo_renta_dice", models.CharField(blank=True, max_length=50)),
                ("obs_tipo_renta_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_tipo_renta",
                    models.CharField(blank=True, default=0, max_length=100),
                ),
                (
                    "respuesta_carrera_semestre",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "obs_carrera_semestre_dice",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "obs_carrera_semestre_debe",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "observacion_carrera_semestre",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "respuesta_profesion",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_profesion_dice", models.CharField(blank=True, max_length=50)),
                ("obs_profesion_debe", models.CharField(blank=True, max_length=50)),
                ("observacion_profesion", models.CharField(blank=True, max_length=100)),
                (
                    "respuesta_estado_civil",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sin Error", "sin error"),
                            ("Error", "error"),
                            ("N/A", "n/a"),
                        ],
                        max_length=20,
                    ),
                ),
                ("obs_estado_civil_dice", models.CharField(blank=True, max_length=50)),
                ("obs_estado_civil_debe", models.CharField(blank=True, max_length=50)),
                (
                    "observacion_estado_civil",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "evaluacion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ficha.evaluacion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("roles", models.CharField(max_length=50)),
                (
                    "foto",
                    models.ImageField(default="default.jpg", upload_to="static/img"),
                ),
                ("ci", models.CharField(max_length=10, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
