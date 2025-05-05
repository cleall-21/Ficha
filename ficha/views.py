from django.shortcuts import render, redirect, get_object_or_404
from .utils import filtro_form
#Import Modelo de tablas User
from django.contrib.auth.models import User
from .models import UserProfile, Registro_materialidad, Evaluacion,EvaluacionFormalidad
# Import Libreria de autentificacion
from django.contrib.auth import authenticate, logout, login as login_auth
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
#Import decorators para impedir ingreso de paginas sin estar registrado
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from django.db import IntegrityError
import pandas as pd
from .forms_evaluacion import (EvaluacionForm, EvaluacionFormalidadForm,
                    EvaluacionGestionOtorgaForm, EvaluacionDepuracionAntecedentesForm)
from .forms import SucursalForm
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
                login(request, us)
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
    form, filtros = filtro_form(request)
    return render(request, 'web/base.html', {'form': form, 'filtros': filtros})

@login_required
def index(request):
    form, filtros = filtro_form(request)
    return render(request, 'web/index.html', {'form': form, 'filtros': filtros})

@login_required
def form_formalidad(request):
    if request.method == "GET":
        return render(request,'web/form_formalidad.html',{'form_evaluacion': EvaluacionFormalidadForm})
    else:
        try:
            form_evaluacion = EvaluacionFormalidadForm(request.POST)
            if form_evaluacion.is_valid():
                new_formalidad = form_evaluacion.save(commit=False)
                new_formalidad.user = request.user
                new_formalidad.save()
                return redirect('form_formalidad')
            else:
                return render(request, 'web/form_formalidad.html', {'form': form_evaluacion, 'error': 'Formulario no válido'})
        except ValueError:
            return render(request, 'web/form_formalidad.html',{'form': EvaluacionFormalidadForm,'error':'Error al crear la Evaluación'})

@login_required
def listar_evaluaciones(request):
    evaluaciones = EvaluacionFormalidad.objects.filter(user=request.user)
    return render(request, 'web/listar_evaluaciones.html', {'evaluaciones': evaluaciones})


@login_required
def detalle_eva(request, id_formalidad):
    if request.method == 'GET':
        eva = get_object_or_404(EvaluacionFormalidad, pk=id_formalidad, user=request.user)
        form = EvaluacionFormalidadForm(instance=eva)
        return render(request, 'web/detalle_eva.html', {'eva': eva, 'form': form})
    else:
        try:
            eva = get_object_or_404(EvaluacionFormalidad, pk=id_formalidad, user=request.user)
            form = EvaluacionFormalidadForm(request.POST, instance=eva)
            form.save()
            return redirect('list_form')
        except ValueError:
            return render(request, 'web/detalle_eva.html', {'eva': eva, 'form': form, 'error': 'Error al modificar la evaluación'})

@login_required
def complete_evaluacion(request, id_formalidad):
    eva = get_object_or_404(EvaluacionFormalidad, pk=id_formalidad, user=request.user)
    eva.completed = True
    eva.save()
    return redirect('list_form')

@login_required
def delete_evaluacion(request, id_formalidad):
    eva = get_object_or_404(EvaluacionFormalidad, pk=id_formalidad, user=request.user)
    eva.delete()
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