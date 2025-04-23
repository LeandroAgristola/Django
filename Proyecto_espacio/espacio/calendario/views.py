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

    # Primer día del mes siguiente
    proximo_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1)
    _, dias_mes_siguiente = monthrange(proximo_mes.year, proximo_mes.month)

    # Último día del mes siguiente
    fin = proximo_mes.replace(day=dias_mes_siguiente)
    dias = (fin - hoy).days + 1

    config = Configuracion.objects.first()
    eventos = []

    for i in range(dias):
        dia_actual = hoy + timedelta(days=i)
        es_sabado = dia_actual.weekday() == 5
        inicio = config.horario_sabado_inicio if es_sabado else config.horario_semana_inicio
        fin_hora = config.horario_sabado_fin if es_sabado else config.horario_semana_fin

        if not (inicio and fin_hora):
            continue

        hora_actual = inicio
        total_disponible = 0

        while hora_actual < fin_hora:
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


