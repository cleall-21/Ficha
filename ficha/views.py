from django.shortcuts import render, redirect, get_object_or_404
#Import Modelo de tablas User
from django.contrib.auth.models import User
from .models import UserProfile, Registro_materialidad, Evaluacion
# Import Libreria de autentificacion
from django.contrib.auth import authenticate, logout, login as login_auth
from django.views.decorators.csrf import csrf_protect
#Import decorators para impedir ingreso de paginas sin estar registrado
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from django.db import IntegrityError
import pandas as pd
from .forms_evaluacion import EvaluacionForm, FormalidadFormSet, GestionOtorgaFormSet, DepuracionAntecedentesFormSet, IngresoDeDatosFormSet
from .forms import SucursalForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404

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

        data = {
            'rut_cliente': oportunidad.rut,
            'nombre_ejec': oportunidad.nombre_ejecutivo,
            'login_ejecutivo': oportunidad.login_creador,
            'rut_ejec':oportunidad.rut_ejecutivo,
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


    if sucursal:
        evaluaciones = evaluaciones.filter(clasificacion__icontains=sucursal)  # Ajusta si tienes un campo específico para sucursal

    # Paginación
    paginator = Paginator(evaluaciones, 5)  # 5 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'web/listar_evaluaciones.html', {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'sucursal': sucursal
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
    return render(request, 'web/listar_ejec.html')

@login_required
def reporte(request):
    return render(request, 'web/reporte.html')

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