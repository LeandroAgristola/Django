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

@login_required
def disponibilidad_por_dia(request):
    hoy = date.today()
    fin = hoy + timedelta(days=60)  # Mostrar 2 meses

    config = Configuracion.objects.first()
    if not config:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=400)

    eventos = []
    actual = hoy

    traduccion_dias = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miercoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sabado',
        'sunday': 'domingo',
    }

    while actual <= fin:
        dia_semana = traduccion_dias[actual.strftime('%A').lower()]

        # Si el día no está habilitado, pasamos al siguiente
        if dia_semana not in config.dias_habilitados:
            actual += timedelta(days=1)
            continue

        # Obtener horarios según el día
        if dia_semana == 'sabado':
            inicio = config.horario_sabado_inicio
            fin_horario = config.horario_sabado_fin
        elif dia_semana == 'domingo':
            inicio = config.horario_domingo_inicio
            fin_horario = config.horario_domingo_fin
        else:
            inicio = config.horario_semana_inicio
            fin_horario = config.horario_semana_fin

        # Calcular turnos disponibles por hora
        total_turnos_disponibles = 0
        hora_actual = inicio

        while hora_actual < fin_horario:
            # Total de turnos por hora (6 por hora)
            turnos_por_hora = 6

            # Turnos ocupados en esta hora
            turnos_ocupados = Turno.objects.filter(fecha=actual, hora=hora_actual).count()

            # Turnos disponibles en esta hora
            turnos_disponibles = turnos_por_hora - turnos_ocupados
            total_turnos_disponibles += turnos_disponibles

            # Avanzar a la siguiente hora
            hora_actual = (datetime.combine(actual, hora_actual) + timedelta(hours=1)).time()

        # Determinar el color del evento
        color = '#28a745' if total_turnos_disponibles > 0 else '#dc3545'

        # Crear el evento
        eventos.append({
            'title': f'{total_turnos_disponibles} turnos disponibles' if total_turnos_disponibles > 0 else 'Sin turnos disponibles',
            'start': actual.isoformat(),
            'color': color,
        })

        actual += timedelta(days=1)

    return JsonResponse(eventos, safe=False)


@login_required
def horarios_por_dia(request):
    fecha_str = request.GET.get('fecha')  # Esperamos formato YYYY-MM-DD
    if not fecha_str:
        return JsonResponse({'error': 'Falta la fecha'}, status=400)

    # Validar formato de la fecha
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)

    # Obtener configuración
    config = Configuracion.objects.first()
    if not config:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=400)

    # Determinar horarios según el día
    es_sabado = fecha.weekday() == 5
    inicio = config.horario_sabado_inicio if es_sabado else config.horario_semana_inicio
    fin = config.horario_sabado_fin if es_sabado else config.horario_semana_fin

    # Si no hay horarios configurados, devolver lista vacía
    if not inicio or not fin:
        return JsonResponse([], safe=False)

    # Calcular horarios disponibles
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


