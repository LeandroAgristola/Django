from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta, date
from django.urls import reverse
from django.contrib import messages
import json
from django.http import JsonResponse

# Importaciones locales
from .models import Cliente
from .forms import ClienteForm
from calendario.models import Turno
from configuracion.models import Configuracion
from planes.models import Plan

@login_required
def lista_clientes(request):
    tipo_filtro = request.GET.get('tipo')
    plan_filtro = request.GET.get('plan')
    estado_filtro = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')

    clientes_activos = Cliente.objects.filter(activo=True)
    clientes_inactivos = Cliente.objects.filter(activo=False)

    if busqueda:
        clientes_activos = clientes_activos.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(dni__icontains=busqueda) |
            Q(mail__icontains=busqueda)
        )
        clientes_inactivos = clientes_inactivos.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(dni__icontains=busqueda) |
            Q(mail__icontains=busqueda)
        )

    if tipo_filtro:
        clientes_activos = clientes_activos.filter(tipo=tipo_filtro)
        clientes_inactivos = clientes_inactivos.filter(tipo=tipo_filtro)

    if plan_filtro:
        clientes_activos = clientes_activos.filter(plan__id=plan_filtro)
        clientes_inactivos = clientes_inactivos.filter(plan__id=plan_filtro)

    if estado_filtro:
        clientes_activos = clientes_activos.filter(estado=estado_filtro)
        clientes_inactivos = clientes_inactivos.filter(estado=estado_filtro)

    planes = Plan.objects.filter(activo=True)

    return render(request, 'clientes/lista_clientes.html', {
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
        'planes': planes,
        'filtros': {
            'busqueda': busqueda or '',
            'tipo': tipo_filtro or '',
            'plan': plan_filtro or '',
            'estado': estado_filtro or ''
        }
    })

@login_required
def crear_cliente(request):
    config = Configuracion.objects.first()
    dias_semana = config.dias_habilitados if config else []
    dias_semana_json = json.dumps(dias_semana) if config else '[]'
    planes_json = json.dumps({str(plan.id): {'cantidad_dias': plan.cantidad_dias} for plan in Plan.objects.filter(activo=True)})

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        dias = request.POST.getlist('dias[]')
        horas = request.POST.getlist('horas[]')

        if form.is_valid():
            try:
                cliente = form.save(commit=False)
                cliente.save()
                
                # Eliminar turnos existentes y generar nuevos
                cliente.turnos.all().delete()
                generar_turnos_futuros(cliente)
                
                messages.success(request, "Cliente creado correctamente.")
                return redirect('clientes:lista_clientes')
                
            except Exception as e:
                print(f"Error al guardar cliente: {str(e)}")
                messages.error(request, f"Error al guardar el cliente: {str(e)}")
        else:
            print(f"Errores de formulario: {form.errors}")
            
        # Preparar datos para rellenar el formulario
        turnos_preseleccionados = []
        dias = request.POST.getlist('dias[]', [])
        horas = request.POST.getlist('horas[]', [])
        
        for dia, hora in zip(dias, horas):
            if dia and hora:
                turnos_preseleccionados.append([dia, hora])
        
        return render(request, 'clientes/forms_cliente.html', {
            'form': form,
            'dias_semana': dias_semana,
            'dias_semana_json': dias_semana_json,
            'planes_json': planes_json,
            'turnos_preseleccionados': turnos_preseleccionados
        })
    
    # GET request
    form = ClienteForm()
    return render(request, 'clientes/forms_cliente.html', {
        'form': form,
        'dias_semana': dias_semana,
        'dias_semana_json': dias_semana_json,
        'planes_json': planes_json
    })

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    config = Configuracion.objects.first()
    dias_semana = config.dias_habilitados if config else []
    dias_semana_json = json.dumps(dias_semana) if config else '[]'
    planes_json = json.dumps({
        str(plan.id): {'cantidad_dias': plan.cantidad_dias}
        for plan in Plan.objects.filter(activo=True)
    })

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)

            # Actualizamos los turnos si vinieron en el POST
            if 'dias[]' in request.POST:
                dias = request.POST.getlist('dias[]')
                horas = request.POST.getlist('horas[]')
                # ... validaciones idénticas ...
                cliente.dias = ", ".join(dias)
                cliente.hora = ", ".join(horas)
                cliente.turnos.all().delete()
                generar_turnos_futuros(cliente)

            # Reactivación: levantamos la baja, PERO no tocamos plan/turnos
            if 'reactivar' in request.GET:
                cliente.activo = True
                cliente.estado = 'pendiente'
                cliente.fecha_baja = None

            cliente.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect('clientes:lista_clientes')

        # Si hay errores:
        return render(request, 'clientes/forms_cliente.html', {
            'form': form,
            'editando': True,
            'reactivando': 'reactivar' in request.GET,
            'dias_semana': dias_semana,
            'dias_semana_json': dias_semana_json,
            'planes_json': planes_json,
        })

    # —————— GET ——————
    # Calculamos la fecha para el input
    if 'reactivar' in request.GET:
        fecha_alta_str = request.GET.get('fecha_alta', '')
        # Limpiar plan y turnos solo en GET para que arranque vacío
        cliente.plan = None
        cliente.dias = ""
        cliente.hora = ""
    else:
        fecha_alta_dt = cliente.fecha_alta
        fecha_alta_str = (
            fecha_alta_dt.strftime('%Y-%m-%d')
            if hasattr(fecha_alta_dt, 'strftime')
            else str(fecha_alta_dt)
        )

    initial_data = {'fecha_alta': fecha_alta_str}
    form = ClienteForm(instance=cliente, initial=initial_data)

    # Pre-cargamos los turnos existentes (si no es reactivación)
    turnos_preseleccionados = []
    if cliente.dias and cliente.hora:
        dias = [d.strip() for d in cliente.dias.split(',')]
        horas = [h.strip() for h in cliente.hora.split(',')]
        turnos_preseleccionados = list(zip(dias, horas))

    return render(request, 'clientes/forms_cliente.html', {
        'form': form,
        'editando': True,
        'reactivando': 'reactivar' in request.GET,
        'dias_semana': dias_semana,
        'dias_semana_json': dias_semana_json,
        'planes_json': planes_json,
        'turnos_preseleccionados': turnos_preseleccionados,
    })

@login_required
def desactivar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        fecha_baja = request.POST.get('fecha_baja')
        
        try:
            fecha_baja_date = datetime.strptime(fecha_baja, "%Y-%m-%d").date()
            
            # 1. Liberar turnos futuros
            cliente.turnos.filter(fecha__gte=fecha_baja_date).delete()
            
            # 2. Limpiar datos del plan
            cliente.plan = None
            cliente.dias = ""
            cliente.hora = ""
            
            # 3. Marcar como inactivo
            cliente.activo = False
            cliente.estado = 'pendiente'
            cliente.fecha_baja = fecha_baja_date
            cliente.save()
            
            messages.success(request, "Cliente desactivado correctamente")
            return redirect('clientes:lista_clientes')
            
        except ValueError:
            messages.error(request, "Formato de fecha inválido")
            return redirect('clientes:lista_clientes')
    
    return redirect('clientes:lista_clientes')


@login_required
def reactivar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    fecha_alta_str = request.POST.get('fecha_alta') or timezone.now().date().strftime("%Y-%m-%d")

    # Solo redirige al formulario con los datos, no reactiva todavía
    redirect_url = reverse('clientes:editar_cliente', kwargs={'cliente_id': cliente.id})
    redirect_url += f'?fecha_alta={fecha_alta_str}&reactivar=1'
    return redirect(redirect_url)

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes:lista_clientes')

@login_required
@require_POST
def confirmar_pago(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.estado = 'confirmado'
    cliente.save()
    return redirect('clientes:lista_clientes')

@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    dias = cliente.dias.split(',') if cliente.dias else []
    horas = cliente.hora.split(',') if cliente.hora else []

    turnos = zip(dias, horas)  # Creamos la lista de tuplas sin asignarla al objeto

    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'turnos': turnos
    })

@login_required
def asignar_turnos(request):
    # Obtener datos del GET o POST
    plan_id = request.GET.get('plan_id') or request.POST.get('plan_id')
    
    # Validar que tenemos plan_id
    if not plan_id:
        messages.error(request, "No se especificó ningún plan")
        return redirect('clientes:crear_cliente')

    # Guardar datos en sesión para posible cancelación
    cliente_data = {
        'nombre': request.GET.get('nombre'),
        'apellido': request.GET.get('apellido'),
        'dni': request.GET.get('dni'),
        'telefono': request.GET.get('telefono'),
        'mail': request.GET.get('mail'),
        'estado': request.GET.get('estado', 'pendiente'),
        'fecha_alta': request.GET.get('fecha_alta'),
        'plan': plan_id
    }
    request.session['cliente_temporal'] = cliente_data

    # Validar campos obligatorios
    required_fields = ['nombre', 'apellido', 'dni', 'mail']
    if not all(cliente_data[field] for field in required_fields):
        messages.error(request, "Faltan datos obligatorios del cliente")
        return redirect('clientes:crear_cliente')

    try:
        plan = Plan.objects.get(id=plan_id)
        config = Configuracion.objects.first()
    except Plan.DoesNotExist:
        messages.error(request, "El plan seleccionado no existe")
        return redirect('clientes:crear_cliente')

    if request.method == 'POST':
        # Procesar el formulario de asignación de turnos
        dias = request.POST.getlist('dias[]')
        horas = request.POST.getlist('horas[]')

        if not dias or not horas:
            messages.error(request, "Debés seleccionar días y horarios.")
            return redirect(request.path + f"?{request.GET.urlencode()}")

        try:
            fecha_alta = datetime.strptime(cliente_data['fecha_alta'], "%Y-%m-%d") if cliente_data['fecha_alta'] else datetime.today()
        except ValueError:
            fecha_alta = datetime.today()

        # Crear o actualizar cliente
        cliente, creado = Cliente.objects.get_or_create(
            mail=cliente_data['mail'],
            defaults={
                'nombre': cliente_data['nombre'],
                'apellido': cliente_data['apellido'],
                'dni': cliente_data['dni'],
                'telefono': cliente_data['telefono'],
                'plan': plan,
                'dias': ", ".join(dias),
                'hora': ", ".join(horas),
                'tipo': 'regular',
                'estado': cliente_data['estado'],
                'fecha_alta': fecha_alta
            }
        )

        if not creado:
            # Actualizar cliente existente
            cliente.nombre = cliente_data['nombre']
            cliente.apellido = cliente_data['apellido']
            cliente.dni = cliente_data['dni']
            cliente.telefono = cliente_data['telefono']
            cliente.plan = plan
            cliente.dias = ", ".join(dias)
            cliente.hora = ", ".join(horas)
            cliente.estado = cliente_data['estado']
            cliente.fecha_alta = fecha_alta
            cliente.save()
            cliente.turnos.all().delete()
        
        generar_turnos_futuros(cliente)
        messages.success(request, "Cliente y turnos asignados correctamente.")
        return redirect('clientes:lista_clientes')

    # Para GET, mostrar formulario de asignación de turnos
    return render(request, 'clientes/asignar_turnos.html', {
        'plan': plan,
        'config': config,
        'dias_semana': config.dias_habilitados if config else [],
        'dias_semana_json': json.dumps(config.dias_habilitados) if config else '[]',
        'initial_data': cliente_data
    })

def generar_turnos_futuros(cliente):
    if not cliente.dias or not cliente.hora:
        return
        
    dias_seleccionados = [dia.strip() for dia in cliente.dias.split(",")]
    horas_seleccionadas = [hora.strip() for hora in cliente.hora.split(",")]
    
    if len(dias_seleccionados) != len(horas_seleccionadas):
        return
        
    fecha_actual = cliente.fecha_alta if cliente.fecha_alta else date.today()
    fecha_limite = fecha_actual + timedelta(days=180)

    dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

    cliente.turnos.filter(fecha__gte=fecha_actual).delete()

    for dia, hora in zip(dias_seleccionados, horas_seleccionadas):
        try:
            dia_idx = dias_esp.index(dia.lower())
            hora_dt = datetime.strptime(hora, "%H:%M").time()
            
            current_date = fecha_actual
            delta_days = (dia_idx - current_date.weekday() + 7) % 7
            current_date += timedelta(days=delta_days)

            while current_date <= fecha_limite:
                ocupados = Turno.objects.filter(
                    fecha=current_date,
                    hora=hora_dt
                ).filter(
                    Q(cliente__fecha_alta__lte=current_date) &
                    (Q(cliente__fecha_baja__isnull=True) | Q(cliente__fecha_baja__gte=current_date))
                ).count()

                if ocupados < 6:
                    Turno.objects.get_or_create(
                        fecha=current_date,
                        hora=hora_dt,
                        cliente=cliente
                    )
                else:
                    print(f"Turno {current_date} {hora_dt} lleno para {cliente}")

                current_date += timedelta(days=7)
        except (ValueError, IndexError):
            continue

@login_required
def clientes_estadisticas(request):
    hoy = timezone.now().date()
    año_actual = hoy.year  # Define año_actual here
    año_actual = hoy.year
    
    # Definimos el rango completo del año calendario
    fecha_inicio = date(año_actual, 1, 1)
    fecha_fin = date(año_actual, 12, 31)
    
    # Nombres de los meses en español
    meses_espanol = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    
    datos = []
    for mes in range(1, 13):
        mes_inicio = date(año_actual, mes, 1)
        mes_fin = date(año_actual, mes+1, 1) if mes < 12 else date(año_actual+1, 1, 1)
        
        # Altas: nuevos clientes en el mes
        altas_nuevos = Cliente.objects.filter(
            fecha_alta__gte=mes_inicio, 
            fecha_alta__lt=mes_fin
        ).count()
        
        # Reactivaciones en el mes (usando el campo modificado como proxy)
        reactivaciones = Cliente.objects.filter(
            activo=True,
            modificado__gte=mes_inicio,
            modificado__lt=mes_fin,
            fecha_baja__isnull=False
        ).count()
        
        altas = altas_nuevos + reactivaciones
        
        # Bajas: desactivados + eliminados en el mes
        bajas = Cliente.objects.filter(
            activo=False,
            fecha_baja__gte=mes_inicio,
            fecha_baja__lt=mes_fin
        ).count()
        
        datos.append({
            'mes': meses_espanol[mes-1],
            'altas': altas,
            'bajas': bajas
        })

    return JsonResponse({
        'labels': [d['mes'] for d in datos],
        'altas': [d['altas'] for d in datos],
        'bajas': [d['bajas'] for d in datos],
        'total_activos': Cliente.objects.filter(activo=True).count(),
        'año': año_actual
    })