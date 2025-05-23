# Generated by Django 5.1.7 on 2025-05-19 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "ficha",
            "0009_alter_evaluacionformalidad_tipo_error_acreditacion_ingresos_and_more",
        ),
    ]

    operations = [
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
    ]
