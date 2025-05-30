from rest_framework import serializers
from .models import Evaluacion, Detalle_evaluaciones

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'

class DetalleEvaluacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_evaluaciones
        fields = '__all__'

