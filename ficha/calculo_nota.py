from .models import Errores_agravante

def calcular_nota(parametro):
    tipo_cliente = parametro.cliente.tipo_cliente
    errores_agravantes = Errores_agravante.objects.filter(parametro=parametro)
    
    notas = []
    if errores_agravantes.exists():
        for agravante in errores_agravantes:
            if agravante.tipo_error == 'No está en carpeta':
                if tipo_cliente in {'Nuevo', 'Prospecto'}:
                    notas.append(2.5)
                elif tipo_cliente in {'Antiguo', 'Plus'}:
                    notas.append(3)
            else:
                notas.append(agravante.nota)
        
        if notas:
            nota_final = min(notas)
        else:
            nota_final = 5  # Valor predeterminado si `notas` está vacío
    else:
        nota_final = 5  # Valor predeterminado si no hay errores agravantes
    
    nota_final = max(1, min(5, nota_final))
    
    error_agravante, created = Errores_agravante.objects.get_or_create(
        tipo_error='Resultado nota final',
        defaults={'nota': nota_final}
    )
    
    if not created:
        error_agravante.nota = nota_final
        error_agravante.save()
   
    return error_agravante

def calcular_nota_final(parametros):
    notas = [parametro.nota.nota for parametro in parametros]
    nota_minima = min(notas)
    
    if nota_minima < 2.5:
        categoria = "Deficiente"
    elif nota_minima < 3:
        categoria = "Insuficiente"
    elif nota_minima < 3.5:
        categoria = "Regular"
    elif nota_minima < 4:
        categoria = "Aceptable"
    elif nota_minima <= 4.9:
        categoria = "Destacado"
    else:
        categoria = "Excelente"
   
    return nota_minima, categoria