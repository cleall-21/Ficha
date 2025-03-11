from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='static/img', default='default.jpg')
    ci = models.CharField(max_length=10, unique=True, validators=[
             RegexValidator(
                regex = r'^\d{7,8}-[\dkK]$',
                  message = "El RUT debe estar en formato 20222777-X"
                        )
                    ],
                    help_text="Formato: 20222777-X"
                        )
    def __str__(self):
        return self.user.username

class Pilares(models.Model):
    id_pilar = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Errores_agravante(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_error = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=5, decimal_places=1)
    def __str__(self):
         return f"{self.tipo_error}"

class Parametro(models.Model):
    id = models.AutoField(primary_key=True)
    pilar = models.ForeignKey(Pilares, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    errores_agravantes = models.ManyToManyField(Errores_agravante, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.pilar}"
    
class sucursal(models.Model):
    cod_sucursal = models.CharField(("Codigo Sucursal"),primary_key=True, max_length=10)
    nombre_suc = models.CharField(("Nombre Sucursal"),max_length=50)
    aprobador = models.CharField(("Nombre aprobador"),max_length=30)
    cant_ejecutivo = models.CharField(("Cantidad Ejecutivos"),max_length=5)

    def __str__(self):
         return self.nombre_suc
    
class oficina(models.Model):
    cui = models.CharField(("CUI"),primary_key=True, max_length=10)
    nombre_ofi = models.CharField(("Nombre Oficina"),max_length=50)  

    def __str__(self):
        return self.nombre_ofi
    
def validar_rut(rut):
    rut = rut.replace(".", "").replace("-","").upper()
    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        raise ValidationError("Solo se adminten caracteres numericos")

    suma = 0
    multiplicador = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    dv_calculado = str(11 - resto) if resto != 0 else "0"
    if dv_calculado =="10":
        dv_calculado = "K"

    if dv != dv_calculado:
                raise ValidationError("El digito verificador del RUT no es válido")
class cliente(models.Model):
    rut = models.CharField(
        primary_key=True,
        max_length=10,
        validators=[
             RegexValidator(
                regex = r'^\d{7,8}-[\dkK]$',
                  message = "El RUT debe estar en formato 20222777-X"
                        )
                    ],
                    help_text="Formato: 20222777-X"
                        )
    oficina = models.ForeignKey(oficina, on_delete=models.CASCADE)
    tipo_producto = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=40)

    def __str__(self):
         return f"{self.rut}"

def val_rut_ejecutivo(rut_ejecutivo):
    rut_ejecutivo = rut_ejecutivo.replace(".", "").replace("-", "").upper()
    if not rut_ejecutivo.isdigit():
        raise ValidationError("Solo se admiten caracteres numéricos")
    return rut_ejecutivo

class ejecutivo(models.Model):
    rut_ejecutivo = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}$',
                message="El RUT debe estar en formato 20222778"
            ),
            val_rut_ejecutivo
        ],
        help_text="Formato: 20222778"
    )
    nombre_ejecutivo = models.CharField(max_length=100)
    username_ejecutivo = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre_ejecutivo}"

class FiltroRevision(models.Model):
    id_filtro = models.AutoField(primary_key=True)
    oficina = models.ForeignKey(oficina, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(sucursal, on_delete=models.CASCADE)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    ejecutivo = models.ForeignKey(ejecutivo, on_delete=models.CASCADE)
    monto_solicitado = models.CharField(max_length=30)
    n_revision = models.IntegerField(('N° Revision'))

    def __str__(self):
        return f"N° de revisión {self.n_revision}"

class Evaluacion(models.Model):
    ejecutivo = models.ForeignKey(ejecutivo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    nota_final = models.DecimalField(max_digits=3, decimal_places=2)
    clasificacion = models.CharField(max_length=50)

    def calcular_nota_final(self):
        detalles = DetalleEvaluacion.objects.filter(evaluacion=self)
        nota_minima = min(detalle.nota for detalle in detalles)
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
class DetalleEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    errores_agravantes = models.ManyToManyField(Errores_agravante, blank=True)
    nota = models.DecimalField(max_digits=3, decimal_places=2)

    def calcular_nota(self):
        notas = [error.nota for error in self.errores_agravantes.all()]
        if notas:
            self.nota = min(notas)
        else:
            self.nota = 5  # Asumiendo que 5 es la nota máxima sin errores
        self.save()

class Registro_materialidad(models.Model):
    id_registro = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    dv = models.CharField(max_length=1)
    log_fecha_registro = models.CharField(max_length=20)
    login_creador = models.CharField(max_length=100)
    nombre_creador = models.CharField(max_length=100)
    oficina_ejecutivo = models.CharField(max_length=100)
    cui = models.CharField(max_length=20)
    etapa_venta_actual = models.CharField(max_length=100)
    inconsistencia = models.CharField(max_length=100)
    monto_oferta = models.CharField(max_length=100)
    proceso_credito = models.CharField(max_length=100)
    pauta_evaluacion = models.CharField(max_length=100)
    decision_final = models.CharField(max_length=100)
    ano_mes = models.CharField(max_length=6)
    canal = models.CharField(max_length=100)
    prod_eval = models.CharField(max_length=100)
    nombre_ejecutivo = models.CharField(max_length=100)
    rut_ejecutivo = models.CharField(max_length=12)
    mes_numero = models.CharField(max_length=12)
    mes_nombre = models.CharField(max_length=20)
    codigo_suc = models.CharField(max_length=10)
    nombre_suc = models.CharField(max_length=100)
    aprobador = models.CharField(max_length=100)
    n_oportunidad = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id_registro}"

#class reporte(models.Model):
    #id_reporte = models.AutoField(primary_key=True)
    #name_reporte = models.CharField(max_length=50)

    #def __str__(self):
        #return f{N° Reporte{self.id_reporte}, {self.name_reporte}}""
