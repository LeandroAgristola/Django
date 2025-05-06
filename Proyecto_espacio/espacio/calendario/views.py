from django.http import JsonResponse
from datetime import timedelta, date, datetime
from .models import Turno
from configuracion.models import Configuracion
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from calendar import monthrange
from django.db.models import Count
import calendar


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

        if dia_semana not in config.dias_habilitados:
            actual += timedelta(days=1)
            continue

        if dia_semana == 'sabado':
            inicio = config.horario_sabado_inicio
            fin_horario = config.horario_sabado_fin
        elif dia_semana == 'domingo':
            inicio = config.horario_domingo_inicio
            fin_horario = config.horario_domingo_fin
        else:
            inicio = config.horario_semana_inicio
            fin_horario = config.horario_semana_fin

        total_turnos_disponibles = 0
        hora_actual = inicio

        while hora_actual < fin_horario:
            ocupados = Turno.objects.filter(fecha=actual,
                hora=hora_actual,
                cliente__activo=True,
                cliente__fecha_alta__lte=actual 
                ).count()

            disponibles = 6 - ocupados
            total_turnos_disponibles += disponibles

            hora_actual = (datetime.combine(actual, hora_actual) + timedelta(hours=1)).time()

        color = '#28a745' if total_turnos_disponibles > 0 else '#dc3545'

        eventos.append({
            'title': f'{total_turnos_disponibles} Turnos' if total_turnos_disponibles > 0 else 'Sin turnos',
            'start': actual.isoformat(),
            'color': color,
        })

        actual += timedelta(days=1)

    return JsonResponse(eventos, safe=False)

@login_required
def horarios_por_dia(request):
    fecha_str = request.GET.get('fecha')
    cliente_id = request.GET.get('cliente_id')

    if not fecha_str:
        return JsonResponse({'error': 'Falta la fecha'}, status=400)

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)

    config = Configuracion.objects.first()
    if not config:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=400)

    dia = fecha.weekday()
    if dia == 5:
        inicio = config.horario_sabado_inicio
        fin = config.horario_sabado_fin
    elif dia == 6:
        inicio = config.horario_domingo_inicio
        fin = config.horario_domingo_fin
    else:
        inicio = config.horario_semana_inicio
        fin = config.horario_semana_fin

    if not inicio or not fin:
        return JsonResponse([], safe=False)

    horarios = []
    hora_actual = inicio

    while hora_actual < fin:
        turnos_qs = Turno.objects.filter(
            fecha=fecha,
            hora=hora_actual,
            cliente__activo=True,
            cliente__fecha_alta__lte=fecha  # 👈 solo clientes activos con fecha válida
        )

        if cliente_id:
            turnos_qs = turnos_qs.exclude(cliente_id=cliente_id)

        ocupados = turnos_qs.count()
        disponibles = 6 - ocupados

        horarios.append({
            'hora': hora_actual.strftime('%H:%M'),
            'disponibles': disponibles,
            'completo': disponibles <= 0
        })

        hora_actual = (datetime.combine(fecha, hora_actual) + timedelta(hours=1)).time()

    return JsonResponse(horarios, safe=False)

@login_required
def detalle_dia(request):
    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return render(request, 'calendario/detalle_dia.html', {'error': 'Fecha no proporcionada'})

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    dia = fecha.weekday()
    config = Configuracion.objects.first()

    if dia == 5:
        inicio = config.horario_sabado_inicio
        fin = config.horario_sabado_fin
    elif dia == 6:
        inicio = config.horario_domingo_inicio
        fin = config.horario_domingo_fin
    else:
        inicio = config.horario_semana_inicio
        fin = config.horario_semana_fin

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


@login_required
def estadisticas_turnos(request):
    hoy = date.today()
    desde = hoy - timedelta(days=30)

    config = Configuracion.objects.first()
    if not config:
        return JsonResponse({'error': 'No hay configuración'}, status=400)

    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    resultado = {dia.capitalize(): {'disponibles': 0, 'ocupados': 0} for dia in dias_semana}

    total_disponibles = 0
    total_ocupados = 0

    for delta in range(30):
        fecha = hoy - timedelta(days=delta)
        dia_index = fecha.weekday()  # 0 = lunes
        dia_nombre = dias_semana[dia_index]
        
        if dia_nombre not in config.dias_habilitados:
            continue

        # Obtener horario según el día
        if dia_nombre == 'sabado':
            inicio = config.horario_sabado_inicio
            fin = config.horario_sabado_fin
        elif dia_nombre == 'domingo':
            inicio = config.horario_domingo_inicio
            fin = config.horario_domingo_fin
        else:
            inicio = config.horario_semana_inicio
            fin = config.horario_semana_fin

        if not inicio or not fin:
            continue

        horas = int((datetime.combine(fecha, fin) - datetime.combine(fecha, inicio)).seconds / 3600)
        posibles_turnos = horas * 6

        ocupados = Turno.objects.filter(fecha=fecha).count()
        disponibles = max(posibles_turnos - ocupados, 0)

        dia_clave = dia_nombre.capitalize()
        resultado[dia_clave]['ocupados'] += ocupados
        resultado[dia_clave]['disponibles'] += disponibles

        total_ocupados += ocupados
        total_disponibles += disponibles

    return JsonResponse({
        'labels': list(resultado.keys()),
        'ocupados': [resultado[d]['ocupados'] for d in resultado],
        'disponibles': [resultado[d]['disponibles'] for d in resultado],
        'total_ocupados': total_ocupados,
        'total_disponibles': total_disponibles,
    })