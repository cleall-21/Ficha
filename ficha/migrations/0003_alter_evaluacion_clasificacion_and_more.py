# Generated by Django 5.1.7 on 2025-05-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ficha", "0002_registro_materialidad_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evaluacion",
            name="clasificacion",
            field=models.CharField(default="Excelente", max_length=15),
        ),
        migrations.AlterField(
            model_name="evaluacion",
            name="nota_final",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
