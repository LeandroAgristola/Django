from django.http import JsonResponse
from datetime import timedelta, date, datetime
from .models import Turno
from configuracion.models import Configuracion
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from calendar import monthrange


@login_required
def vista_calendario(request):
    return render(request, 'calendario/calendario.html')

#Esta vista genera eventos para el calendario, indicando la disponibilidad de horarios por día.
#Lógica clave:
#Calcula los días desde hoy hasta el final del mes siguiente.
#Determina los horarios disponibles por día basándose en la configuración (Configuracion) y los turnos ya ocupados.
#Asigna un color (#dc3545 para no disponible y #28a745 para disponible) y un título con la cantidad de horarios disponibles.
@login_required
def disponibilidad_por_dia(request):
    config = Configuracion.objects.first()
    eventos = []

    # Intenta obtener el rango del calendario (usado por FullCalendar)
    inicio_str = request.GET.get('start')
    fin_str = request.GET.get('end')

    try:
        inicio = datetime.strptime(inicio_str[:10], "%Y-%m-%d").date() if inicio_str else date.today()
        fin = datetime.strptime(fin_str[:10], "%Y-%m-%d").date() if fin_str else (inicio.replace(day=28) + timedelta(days=4)).replace(day=1)
    except ValueError:
        return JsonResponse({'error': 'Fechas inválidas'}, status=400)

    dias = (fin - inicio).days + 1

    for i in range(dias):
        dia_actual = inicio + timedelta(days=i)
        es_sabado = dia_actual.weekday() == 5
        hora_inicio = config.horario_sabado_inicio if es_sabado else config.horario_semana_inicio
        hora_fin = config.horario_sabado_fin if es_sabado else config.horario_semana_fin

        if not (hora_inicio and hora_fin):
            continue

        total_disponible = 0
        hora_actual = hora_inicio

        while hora_actual < hora_fin:
            cantidad = Turno.objects.filter(fecha=dia_actual, hora=hora_actual).count()
            if cantidad < 6:
                total_disponible += 1
            hora_actual = (datetime.combine(date.today(), hora_actual) + timedelta(hours=1)).time()

        color = '#dc3545' if total_disponible == 0 else '#28a745'
        eventos.append({
            'title': f"{total_disponible} horarios",
            'start': dia_actual.isoformat(),
            'color': color,
        })

    return JsonResponse(eventos, safe=False)

#Esta vista devuelve los horarios disponibles para un día específico.
#Lógica clave:
#Obtiene la fecha desde los parámetros GET.
#Calcula los horarios disponibles basándose en la configuración (Configuracion) y los turnos ya ocupados.
#Devuelve un JSON con los horarios, indicando cuántos espacios están disponibles y si el horario está completo.
@login_required
def horarios_por_dia(request):
    fecha_str = request.GET.get('fecha')  # Esperamos formato YYYY-MM-DD
    if not fecha_str:
        return JsonResponse({'error': 'Falta la fecha'}, status=400)

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    es_sabado = fecha.weekday() == 5

    config = Configuracion.objects.first()
    inicio = config.horario_sabado_inicio if es_sabado else config.horario_semana_inicio
    fin = config.horario_sabado_fin if es_sabado else config.horario_semana_fin

    horarios = []
    hora_actual = inicio

    while hora_actual < fin:
        cantidad = Turno.objects.filter(fecha=fecha, hora=hora_actual).count()
        disponible = 6 - cantidad
        horarios.append({
            'hora': hora_actual.strftime('%H:%M'),
            'disponibles': disponible,
            'completo': disponible == 0
        })
        hora_actual = (datetime.combine(fecha, hora_actual) + timedelta(hours=1)).time()

    return JsonResponse(horarios, safe=False)


#Esta vista muestra un desglose detallado de los turnos para un día específico.
#Lógica clave:
#Obtiene la fecha desde los parámetros GET.
#Genera una grilla con los turnos ocupados y los espacios disponibles para cada hora.
#Devuelve un template con la información detallada.
@login_required
def detalle_dia(request):
    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return render(request, 'calendario/detalle_dia.html', {'error': 'Fecha no proporcionada'})

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    es_sabado = fecha.weekday() == 5
    config = Configuracion.objects.first()
    inicio = config.horario_sabado_inicio if es_sabado else config.horario_semana_inicio
    fin = config.horario_sabado_fin if es_sabado else config.horario_semana_fin

    grilla = []
    hora_actual = inicio

    while hora_actual < fin:
        turnos = Turno.objects.filter(fecha=fecha, hora=hora_actual).select_related('cliente').order_by('id')
        fila = []
        for i in range(6):
            if i < len(turnos):
                cliente = turnos[i].cliente
                fila.append({
                    'numero': i+1,
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido,
                    'telefono': cliente.telefono
                })
            else:
                fila.append({
                    'numero': i+1,
                    'nombre': None
                })

        grilla.append({
            'hora': hora_actual.strftime('%H:%M'),
            'turnos': fila
        })

        hora_actual = (datetime.combine(fecha, hora_actual) + timedelta(hours=1)).time()

    return render(request, 'calendario/detalle_dia.html', {
        'fecha': fecha,
        'grilla': grilla
    })


