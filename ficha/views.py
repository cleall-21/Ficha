from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Registro_materialidad, Evaluacion, Detalle_evaluaciones,actualizar_detalle_evaluaciones
# Import Libreria de autentificacion
from django.contrib.auth import authenticate, logout, login as login_auth
from django.views.decorators.csrf import csrf_protect
#Import decorators para impedir ingreso de paginas sin estar registrado
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from django.db import IntegrityError
import pandas as pd
import json
from .forms_evaluacion import EvaluacionForm, FormalidadFormSet, GestionOtorgaFormSet, DepuracionAntecedentesFormSet, IngresoDeDatosFormSet
from .forms import SucursalForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
import requests 
from ficha.tabla_resumen import calculo_tabla, extraer_observaciones, porcentaje_cumplimiento,porcentaje_cumplimiento_por_campo
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Evaluacion, Detalle_evaluaciones
from .serializers import EvaluacionSerializer, DetalleEvaluacionesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status

# API para llamar al calculo de la nota al frontend
class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'codigo_sucursal': ['exact'],
        'fecha': ['gte', 'lte'],
    }

    @action(detail=True, methods=['POST'])
    def calcular(self, request, pk=None):
        evaluacion = self.get_object()
        evaluacion.calcular_nota_final()

        # Actualizar el resumen por sucursal
        try:
            actualizar_detalle_evaluaciones(
                codigo_sucursal=evaluacion.codigo_sucursal,
                nota_automatica=('0')  # o algún valor por defecto
            )
        except Exception as e:
            print(f"Error al actualizar detalle de sucursal: {e}")

        serializer = self.get_serializer(evaluacion)
        return Response(serializer.data)

class DetalleEvaluacionesViewSet(viewsets.ModelViewSet):
    queryset = Detalle_evaluaciones.objects.all()
    serializer_class = DetalleEvaluacionesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'codigo_sucursal': ['exact'],
    }

    @action(detail=True, methods=['post'])
    def calcular(self, request, pk=None):
        nota_automatica = request.data.get('nota_automatica')

        if nota_automatica is None:
            return Response({'error': 'nota_automatica es requerida'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            detalle, created = actualizar_detalle_evaluaciones(
                codigo_sucursal=pk,
                nota_automatica=nota_automatica
            ) # type: ignore

            if detalle is None:
                return Response({'error': 'No hay evaluaciones para esta sucursal'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(detalle)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def registro(request):
    if request.method == 'POST':
        nombres = request.POST.get("nombres").strip()
        apellidos = request.POST.get("apellidos").strip()
        email = request.POST.get("email").strip()
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        password2 = request.POST.get("password2").strip()
        roles = request.POST.get("roles").strip()

        # Validar que el correo no esté en uso
        if User.objects.filter(email=email).exists():
            message = "El correo ya está en uso"
            return render(request, 'web/registro.html', {'Error': message})

        # Validar que las contraseñas coincidan
        if password != password2:
            message = "Las contraseñas no coinciden"
            return render(request, 'web/registro.html', {'Error': message})

        try:
            # Intentar crear un nuevo usuario
            u = User.objects.create_user(username=username, email=email, password=password, first_name=nombres, last_name=apellidos)
            # Crear el perfil de usuario
            perfil = UserProfile(user=u, roles=roles)
            perfil.save()
            u.save()
            mensaje = "Registro exitoso"
            # Autenticar y loguear al usuario
            us = authenticate(request, username=username, password=password)
            if us is not None:
                login(request, us) # type: ignore
                return redirect('index')  # Redirigir a la página de inicio o dashboard
            else:
                mensaje = "Error en la autenticación"
                return render(request, 'web/login.html', {'Error': mensaje})
        except IntegrityError:
            # Si el usuario ya existe, manejar la excepción y mostrar el mensaje de error
            mensaje = "Usuario existente"
            return render(request, 'web/registro.html', {'Error': mensaje})

    # Renderizar la página de registro si el método no es POST
    return render(request, 'web/registro.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            message = "Usuario y contraseña son obligatorios."
            return render(request, 'web/login.html', {'error': message})
        
        us = authenticate(request, username=username, password=password)
        if us is not None and us.is_active:
            login_auth(request, us)
            return redirect('index')
        else:
            message = "Usuario o contraseña incorrectos"
            return render(request, 'web/login.html', {'error': message})
    return render(request, 'web/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirigir a la vista de inicio de sesión

@login_required
def base(request):
    return render(request, 'web/base.html')

def obtener_datos_oportunidad(request, rut):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            oportunidad = Registro_materialidad.objects.filter(rut=rut).latest('log_fecha_registro')
        except Registro_materialidad.DoesNotExist:
            return JsonResponse({'error': 'Oportunidad no encontrada'}, status=404)

        # Concatenar el RUT con el dígito verificador
        rut_completo = f"{oportunidad.rut}-{oportunidad.dv}"

        data = {
            'rut_cliente': rut_completo,
            'nombre_ejec': oportunidad.nombre_ejecutivo,
            'login_ejecutivo': oportunidad.login_creador,
            'rut_ejec': oportunidad.rut_ejecutivo,
            'sucursal': oportunidad.nombre_suc,
            'codigo_sucursal': oportunidad.codigo_suc,
            'producto': oportunidad.prod_eval,
            'monto_solicitado': oportunidad.monto_oferta,
            'proceso_credito': oportunidad.proceso_credito,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)

@login_required
def buscar_oportunidad(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            codigo_suc = form.cleaned_data['codigo_suc']
            nombre_ejecutivo = form.cleaned_data.get('nombre_ejecutivo')
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')

            # Si no se seleccionó nombre_ejecutivo, devolvemos solo la lista de ejecutivos
            if not nombre_ejecutivo:
                queryset = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
                if fecha_inicio and fecha_fin:
                    queryset = queryset.filter(log_fecha_registro__range=[fecha_inicio, fecha_fin])
                nombres = queryset.values_list('nombre_ejecutivo', flat=True).distinct()
                return JsonResponse({'ejecutivos': list(nombres)})

            # Si hay nombre_ejecutivo, hacemos la búsqueda completa
            filtros = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
            if fecha_inicio and fecha_fin:
                filtros = filtros.filter(log_fecha_registro__range=[fecha_inicio, fecha_fin])
            if nombre_ejecutivo:
                filtros = filtros.filter(nombre_ejecutivo=nombre_ejecutivo)

            # Paginación
            page_number = request.GET.get('page', 1)
            paginator = Paginator(filtros, 3)
            page_obj = paginator.get_page(page_number)

            html = render_to_string('web/resultados.html', {
                'filtros': page_obj,
                'paginator': paginator,
                'page_obj': page_obj
            })

            return JsonResponse({'html': html})
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def index(request):
    filtros = None
    sucursal_form = SucursalForm(request.POST or None)

    if request.method == 'POST' and 'codigo_suc' in request.POST:
        if sucursal_form.is_valid():
            codigo_suc = sucursal_form.cleaned_data['codigo_suc']
            nombre_ejecutivo = sucursal_form.cleaned_data.get('nombre_ejecutivo')
            fecha_inicio = sucursal_form.cleaned_data.get('fecha_inicio')
            fecha_fin = sucursal_form.cleaned_data.get('fecha_fin')

            filtros = Registro_materialidad.objects.filter(codigo_suc=codigo_suc)
            if fecha_inicio and fecha_fin:
                filtros = filtros.filter(fecha__range=[fecha_inicio, fecha_fin])
            if nombre_ejecutivo:
                filtros = filtros.filter(nombre_ejecutivo=nombre_ejecutivo)

    # Formularios de evaluación
    if request.method == 'POST' and 'codigo_suc' not in request.POST:
        evaluacion_form = EvaluacionForm(request.POST)
        formalidad_formset = FormalidadFormSet(request.POST, instance=evaluacion_form.instance)
        gestion_otorga_formset = GestionOtorgaFormSet(request.POST, instance=evaluacion_form.instance)
        depuracion_antecedentes_formset = DepuracionAntecedentesFormSet(request.POST, instance=evaluacion_form.instance)
        ingreso_datos_formset = IngresoDeDatosFormSet(request.POST, instance=evaluacion_form.instance)

        if evaluacion_form.is_valid() and formalidad_formset.is_valid() and gestion_otorga_formset.is_valid() and depuracion_antecedentes_formset.is_valid() and ingreso_datos_formset.is_valid():
            evaluacion = evaluacion_form.save(commit=False)
            evaluacion.user = request.user
            evaluacion.save()

            formalidad_formset.instance = evaluacion
            formalidad_formset.save()

            gestion_otorga_formset.instance = evaluacion
            gestion_otorga_formset.save()

            depuracion_antecedentes_formset.instance = evaluacion
            depuracion_antecedentes_formset.save()

            ingreso_datos_formset.instance = evaluacion
            ingreso_datos_formset.save()

            return redirect('index')
    else:
        evaluacion_form = EvaluacionForm()
        formalidad_formset = FormalidadFormSet(instance=evaluacion_form.instance)
        gestion_otorga_formset = GestionOtorgaFormSet(instance=evaluacion_form.instance)
        depuracion_antecedentes_formset = DepuracionAntecedentesFormSet(instance=evaluacion_form.instance)
        ingreso_datos_formset = IngresoDeDatosFormSet(instance=evaluacion_form.instance)

    return render(request, 'web/index.html', {
        'form': sucursal_form,
        'filtros': filtros,
        'evaluacion_form': evaluacion_form,
        'formalidad_formset': formalidad_formset,
        'gestion_otorga_formset': gestion_otorga_formset,
        'depuracion_antecedentes_formset': depuracion_antecedentes_formset,
        'ingreso_datos_formset': ingreso_datos_formset
    })

@login_required
def listar_evaluaciones(request):
    evaluaciones = Evaluacion.objects.filter(user=request.user)

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    sucursal = request.GET.get('sucursal')

    if fecha_inicio:
        evaluaciones = evaluaciones.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        evaluaciones = evaluaciones.filter(fecha__lte=fecha_fin)
    if sucursal:
        evaluaciones = evaluaciones.filter(codigo_sucursal__icontains=sucursal)

    codigos_validos = list(
        Evaluacion.objects.filter(user=request.user)
        .values_list('codigo_sucursal', flat=True)
        .distinct()
    )

    # Paginación
    paginator = Paginator(evaluaciones, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'web/listar_evaluaciones.html', {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'sucursal': sucursal,
        'codigos_validos': json.dumps(codigos_validos),
    })

@login_required
def detalle_eva(request, id_evaluacion):
    evaluacion = get_object_or_404(Evaluacion, pk=id_evaluacion, user=request.user)

    if request.method == 'POST':
        evaluacion_form = EvaluacionForm(request.POST, instance=evaluacion)
        formalidad_formset = FormalidadFormSet(request.POST, instance=evaluacion)
        gestion_otorga_formset = GestionOtorgaFormSet(request.POST, instance=evaluacion)
        depuracion_antecedentes_formset = DepuracionAntecedentesFormSet(request.POST, instance=evaluacion)
        ingreso_datos_formset = IngresoDeDatosFormSet(request.POST, instance=evaluacion)

        if (evaluacion_form.is_valid() and formalidad_formset.is_valid() and
            gestion_otorga_formset.is_valid() and depuracion_antecedentes_formset.is_valid() and
            ingreso_datos_formset.is_valid()):
            
            evaluacion_form.save()
            formalidad_formset.save()
            gestion_otorga_formset.save()
            depuracion_antecedentes_formset.save()
            ingreso_datos_formset.save()

            return redirect('list_form')
        else:
            return render(request, 'web/detalle_eva.html', {
                'eva': evaluacion,  
                'evaluacion_form': evaluacion_form,
                'formalidad_formset': formalidad_formset,
                'gestion_otorga_formset': gestion_otorga_formset,
                'depuracion_antecedentes_formset': depuracion_antecedentes_formset,
                'ingreso_datos_formset': ingreso_datos_formset,
                'error': 'Formulario no válido'
            })

    else:
        evaluacion_form = EvaluacionForm(instance=evaluacion)
        formalidad_formset = FormalidadFormSet(instance=evaluacion)
        gestion_otorga_formset = GestionOtorgaFormSet(instance=evaluacion)
        depuracion_antecedentes_formset = DepuracionAntecedentesFormSet(instance=evaluacion)
        ingreso_datos_formset = IngresoDeDatosFormSet(instance=evaluacion)

        return render(request, 'web/detalle_eva.html', {
            'eva': evaluacion, 
            'evaluacion_form': evaluacion_form,
            'formalidad_formset': formalidad_formset,
            'gestion_otorga_formset': gestion_otorga_formset,
            'depuracion_antecedentes_formset': depuracion_antecedentes_formset,
            'ingreso_datos_formset': ingreso_datos_formset
        })

@login_required
def delete_evaluacion(request, id_evaluacion):
    evaluacion = get_object_or_404(Evaluacion, pk=id_evaluacion, user=request.user)
    evaluacion.delete()
    return redirect('list_form')

@login_required
def listar_ejec(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    sucursal = request.GET.get('sucursal')

    evaluaciones = Evaluacion.objects.filter(user=request.user)

    if fecha_inicio:
        evaluaciones = evaluaciones.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        evaluaciones = evaluaciones.filter(fecha__lte=fecha_fin)
    if sucursal:
        evaluaciones = evaluaciones.filter(codigo_sucursal__icontains=sucursal)

    resumen = calculo_tabla(evaluaciones)

    totales = {
        'Deficiente': 0,
        'Insuficiente': 0,
        'Regular': 0,
        'Aceptable': 0,
        'Destacado': 0,
        'Excelente': 0,
        'Total_Calificaciones': 0
    }

    for datos in resumen.values():
        for clave in totales:
            totales[clave] += datos.get(clave, 0) # type: ignore

    codigos_validos = list(
        Evaluacion.objects.filter(user=request.user)
        .values_list('codigo_sucursal', flat=True)
        .distinct()
    )

    # Extraer observaciones relevantes
    observaciones_relevantes = []
    for evaluacion in evaluaciones:
        observaciones_relevantes.extend(extraer_observaciones(evaluacion))

    return render(request, 'web/listar_ejec.html', {
        'resumen': resumen,
        'sucursal': sucursal,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'totales': totales,
        'codigos_validos': json.dumps(codigos_validos),
        'observaciones': observaciones_relevantes  
    })

@login_required
def reporte(request):
    # Obtener filtro desde GET
    codigo_sucursal = request.GET.get('codigo_sucursal')

    # Filtrar evaluaciones si se especifica código de sucursal
    evaluaciones = Evaluacion.objects.all()
    if codigo_sucursal:
        evaluaciones = evaluaciones.filter(codigo_sucursal=codigo_sucursal)

    # Calcular cumplimiento por pilar (gráfico principal)
    cumplimiento_por_pilar = porcentaje_cumplimiento(evaluaciones)

    # Calcular cumplimiento por campo (gráficos secundarios)
    cumplimiento_por_campo = porcentaje_cumplimiento_por_campo(evaluaciones)

    # Obtener lista de códigos de sucursal únicos
    codigos_sucursal = Evaluacion.objects.values_list('codigo_sucursal', flat=True).distinct()

    # Preparar contexto para la plantilla
    context = {
        'datos_cumplimiento': json.dumps(cumplimiento_por_pilar),  # Para gráfico principal
        'datos_por_campo': json.dumps(cumplimiento_por_campo),     # Para gráficos por campo
        'codigos_sucursal': codigos_sucursal,
        'codigo_seleccionado': codigo_sucursal
    }

    return render(request, 'web/reporte.html', context)

def es_valido(row):
    # Ejemplo de validación: verificar que el RUT no esté vacío
    return row['RUT'] != ''

def limpiar_valor(valor):
    # Convertir el valor a cadena y eliminar espacios en blanco
    return str(valor).strip()

@login_required
def carga_materialidad(request):
    if request.method == 'POST' and request.FILES['archivo']:
        archivo_excel = request.FILES['archivo']
        try:
            df = pd.read_excel(archivo_excel, dtype=str)  # Leer todo como cadenas
            # Limpiar el DataFrame eliminando filas con todos los valores NaN
            df.dropna(how='all', inplace=True)
            # Rellenar valores NaN con una cadena vacía
            df.fillna('', inplace=True)
        except Exception as e:
            return HttpResponse(f"Error al leer el archivo: {e}")

        errores = []
        registros = []
        for _, row in df.iterrows():
            if not es_valido(row):
                errores.append(f"Datos inválidos en la fila {_}")
                continue
            try:
                registros.append(Registro_materialidad(
                    rut=limpiar_valor(row['RUT']),
                    dv=limpiar_valor(row['DV']),
                    log_fecha_registro=limpiar_valor(row['LOG_FECHA_REGISTRO']),
                    login_creador=limpiar_valor(row['LOGIN CREADOR']),
                    nombre_ejecutivo=limpiar_valor(row['NOMBRE EJECUTIVO']),
                    rut_ejecutivo=limpiar_valor(row['RUT EJECUTIVO']),
                    oficina_ejecutivo=limpiar_valor(row['OFICINA_EJECUTIVO']),
                    cui=limpiar_valor(row['CUI']),
                    etapa_venta_actual=limpiar_valor(row['ETAPA_VENTA_ACTUAL']),
                    inconsistencia=limpiar_valor(row['INCONSISTENCIA']),
                    max_prod_rgo=limpiar_valor(row['MAX_PROD_RGO']),
                    monto_oferta=limpiar_valor(row['MONTO_OFERTA']),
                    proceso_credito=limpiar_valor(row['PROCESO_CREDITO']),
                    pauta_evaluacion=limpiar_valor(row['PAUTA_EVALUACION']),
                    ano_mes=limpiar_valor(row['AÑO MES']),
                    canal=limpiar_valor(row['CANAL']),
                    prod_eval=limpiar_valor(row['PROD_EVAL']),
                    mes_nombre=limpiar_valor(row['MES_NOMBRE']),
                    estado=limpiar_valor(row['ESTADO']),
                    codigo_suc=limpiar_valor(row['CODIGO_SUC']),
                    nombre_suc=limpiar_valor(row['NOMBRE_SUC']),
                    aprobador=limpiar_valor(row['APROBADOR']),
                    id_oportunidad=limpiar_valor(row['ID_OPORTUNIDAD'])
                ))
            except Exception as e:
                errores.append(f"Error en la fila {_}: {e}")

        if registros:
            Registro_materialidad.objects.bulk_create(registros)

        if errores:
            return HttpResponse(f"Errores encontrados: {', '.join(errores)}")
        return HttpResponse("Datos cargados exitosamente")
    return render(request, 'web/carga_materialidad.html')

def vista_evaluaciones_api(request):
    try:
        response_eval = requests.get('http://127.0.0.1:8000/evaluaciones/')
        response_detalle = requests.get('http://127.0.0.1:8000/detalle-evaluaciones/')

        if response_eval.status_code == 200:
            evaluaciones = response_eval.json()
        else:
            evaluaciones = []
            print("Error al obtener evaluaciones:", response_eval.status_code)

        if response_detalle.status_code == 200:
            detalles = response_detalle.json()
        else:
            detalles = []
            print("Error al obtener detalles:", response_detalle.status_code)

    except Exception as e:
        evaluaciones = []
        detalles = []
        print("Error al obtener datos:", e)

    return render(request, 'web/calculo_nota.html', {
        'evaluaciones': evaluaciones,
        'detalles': detalles
    })
