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
from .models import Cliente
from .forms import ClienteForm
from calendario.models import Turno
from configuracion.models import Configuracion
from planes.models import Plan
from django.core.management import call_command


@login_required
def lista_clientes(request):
    """
    Vista principal que lista clientes con filtros:
    - Filtros por tipo, plan, estado y búsqueda
    - Separa clientes activos/inactivos
    - Incluye datos para filtros en template
    """
    # Obtener parámetros de filtrado
    tipo_filtro = request.GET.get('tipo')
    plan_filtro = request.GET.get('plan')
    estado_filtro = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')

    # QuerySets base
    clientes_activos = Cliente.objects.filter(activo=True)
    clientes_inactivos = Cliente.objects.filter(activo=False)

    # Aplicar filtros de búsqueda
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

    # Aplicar filtros adicionales
    if tipo_filtro:
        clientes_activos = clientes_activos.filter(tipo=tipo_filtro)
        clientes_inactivos = clientes_inactivos.filter(tipo=tipo_filtro)

    if plan_filtro:
        clientes_activos = clientes_activos.filter(plan__id=plan_filtro)
        clientes_inactivos = clientes_inactivos.filter(plan__id=plan_filtro)

    if estado_filtro:
        clientes_activos = clientes_activos.filter(estado=estado_filtro)
        clientes_inactivos = clientes_inactivos.filter(estado=estado_filtro)

    # Obtener planes para filtros
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
    """
    Vista para crear nuevo cliente:
    - Maneja formulario con validaciones
    - Asigna turnos según plan
    - Genera turnos futuros automáticamente
    """
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
        
        # Preparar datos para mostrar errores    
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
    
    # GET: Mostrar formulario vacío
    form = ClienteForm()
    return render(request, 'clientes/forms_cliente.html', {
        'form': form,
        'dias_semana': dias_semana,
        'dias_semana_json': dias_semana_json,
        'planes_json': planes_json
    })

@login_required
def editar_cliente(request, cliente_id):
    """
    Vista para editar cliente existente:
    - Maneja reactivación de clientes inactivos
    - Actualiza turnos al guardar cambios
    - Mantiene datos de días/horarios seleccionados
    """
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

            # Actualizar turnos si se modificaron días/horarios
            if 'dias[]' in request.POST:
                dias = request.POST.getlist('dias[]')
                horas = request.POST.getlist('horas[]')
                cliente.dias = ", ".join(dias)
                cliente.hora = ", ".join(horas)
                cliente.turnos.all().delete()
                generar_turnos_futuros(cliente)

            # Manejar reactivación
            if 'reactivar' in request.GET:
                cliente.activo = True
                cliente.estado = 'pendiente'
                cliente.fecha_baja = None

            cliente.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect('clientes:lista_clientes')

        return render(request, 'clientes/forms_cliente.html', {
            'form': form,
            'editando': True,
            'reactivando': 'reactivar' in request.GET,
            'dias_semana': dias_semana,
            'dias_semana_json': dias_semana_json,
            'planes_json': planes_json,
        })
    
    # GET: Mostrar formulario con datos actuales
    if 'reactivar' in request.GET:
        fecha_alta_str = request.GET.get('fecha_alta', '')
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

    # Preparar turnos preseleccionados para mostrar en UI
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
    """
    Vista para desactivar cliente:
    - Establece fecha de baja
    - Elimina turnos futuros
    - Limpia datos de plan y turnos
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        fecha_baja = request.POST.get('fecha_baja')
        
        try:
            fecha_baja_date = datetime.strptime(fecha_baja, "%Y-%m-%d").date()

            # Eliminar turnos futuros
            cliente.turnos.filter(fecha__gte=fecha_baja_date).delete()

            # Limpiar datos
            cliente.plan = None
            cliente.dias = ""
            cliente.hora = ""

            # Marcar como inactivo
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
    """
    Vista para redirigir a edición con opción de reactivación:
    - Prepara datos para formulario de edición
    - Permite establecer nueva fecha de alta
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)

    fecha_alta_str = request.POST.get('fecha_alta') or timezone.now().date().strftime("%Y-%m-%d")

    redirect_url = reverse('clientes:editar_cliente', kwargs={'cliente_id': cliente.id})
    redirect_url += f'?fecha_alta={fecha_alta_str}&reactivar=1'
    return redirect(redirect_url)

@login_required
def eliminar_cliente(request, cliente_id):
    """
    Vista para eliminar cliente permanentemente
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes:lista_clientes')

@login_required
@require_POST
def confirmar_pago(request, cliente_id):
    """
    Vista para confirmar pago de cliente:
    - Actualiza estado y fecha de confirmación
    - Solo para clientes regulares
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.estado = 'confirmado'
    cliente.ultima_confirmacion = timezone.now().date()
    cliente.save()
    messages.success(request, f"Pago confirmado para {cliente.nombre}")
    return redirect('clientes:lista_clientes')

@login_required
def detalle_cliente(request, cliente_id):
    """
    Vista para mostrar detalles de cliente:
    - Información básica
    - Turnos asignados
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    dias = cliente.dias.split(',') if cliente.dias else []
    horas = cliente.hora.split(',') if cliente.hora else []

    turnos = zip(dias, horas)  

    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'turnos': turnos
    })

@login_required
def asignar_turnos(request):
    """
    Vista especializada para asignación de turnos:
    - Maneja un flujo de dos pasos: datos del cliente + asignación de turnos
    - Valida datos del cliente y disponibilidad de turnos
    - Genera turnos futuros automáticamente según plan
    - Usa sesión para mantener datos temporales del cliente
    """
    # Obtener ID del plan desde GET o POST
    plan_id = request.GET.get('plan_id') or request.POST.get('plan_id')
    
    if not plan_id:
        messages.error(request, "No se especificó ningún plan")
        return redirect('clientes:crear_cliente')
    
    # Recopilar datos del cliente desde el request
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
    # Guardar datos en sesión para persistencia
    request.session['cliente_temporal'] = cliente_data

    # Validar campos obligatorios
    required_fields = ['nombre', 'apellido', 'dni', 'mail']
    if not all(cliente_data[field] for field in required_fields):
        messages.error(request, "Faltan datos obligatorios del cliente")
        return redirect('clientes:crear_cliente')

    try:
        # Obtener objetos relacionados
        plan = Plan.objects.get(id=plan_id)
        config = Configuracion.objects.first()
    except Plan.DoesNotExist:
        messages.error(request, "El plan seleccionado no existe")
        return redirect('clientes:crear_cliente')
    
    # Manejar POST (envío del formulario de turnos)
    if request.method == 'POST':
        dias = request.POST.getlist('dias[]')
        horas = request.POST.getlist('horas[]')

        # Validar selección de días/horarios
        if not dias or not horas:
            messages.error(request, "Debés seleccionar días y horarios.")
            return redirect(request.path + f"?{request.GET.urlencode()}")
        
        # Procesar fecha de alta
        try:
            fecha_alta = datetime.strptime(cliente_data['fecha_alta'], "%Y-%m-%d") if cliente_data['fecha_alta'] else datetime.today()
        except ValueError:
            fecha_alta = datetime.today()

        # Crear o actualizar cliente
        cliente, creado = Cliente.objects.get_or_create(
            mail=cliente_data['mail'], # Usar email como identificador único
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

        # Actualizar cliente existente si es necesario
        if not creado:
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
            cliente.turnos.all().delete()  # Eliminar turnos existentes para regenerarlos
        
        # Generar turnos futuros según la configuración
        generar_turnos_futuros(cliente)
        messages.success(request, "Cliente y turnos asignados correctamente.")
        return redirect('clientes:lista_clientes')
    
    # GET: Mostrar formulario de asignación de turnos
    return render(request, 'clientes/asignar_turnos.html', {
        'plan': plan,
        'config': config,
        'dias_semana': config.dias_habilitados if config else [], # Días habilitados según configuración
        'dias_semana_json': json.dumps(config.dias_habilitados) if config else '[]',# Datos para JS
        'initial_data': cliente_data # Datos del cliente para prellenar
    })

def generar_turnos_futuros(cliente):
    """
    Función auxiliar para generar turnos futuros:
    - Crea turnos semanales según días/horarios asignados
    - Considera disponibilidad (máx 6 turnos por hora)
    - Genera turnos por 6 meses (180 días)
    """
    if not cliente.dias or not cliente.hora:
        return
        
    dias_seleccionados = [dia.strip() for dia in cliente.dias.split(",")]
    horas_seleccionadas = [hora.strip() for hora in cliente.hora.split(",")]
    
    if len(dias_seleccionados) != len(horas_seleccionadas):
        return
        
    fecha_actual = cliente.fecha_alta if cliente.fecha_alta else date.today()
    fecha_limite = fecha_actual + timedelta(days=180)

    dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

    # Eliminar turnos futuros existentes
    cliente.turnos.filter(fecha__gte=fecha_actual).delete()

    # Generar nuevos turnos
    for dia, hora in zip(dias_seleccionados, horas_seleccionadas):
        try:
            dia_idx = dias_esp.index(dia.lower())
            hora_dt = datetime.strptime(hora, "%H:%M").time()
            
            current_date = fecha_actual
            delta_days = (dia_idx - current_date.weekday() + 7) % 7
            current_date += timedelta(days=delta_days)

            # Generar turnos semanales hasta fecha límite
            while current_date <= fecha_limite:
                ocupados = Turno.objects.filter(
                    fecha=current_date,
                    hora=hora_dt
                ).filter(
                    Q(cliente__fecha_alta__lte=current_date) &
                    (Q(cliente__fecha_baja__isnull=True) | Q(cliente__fecha_baja__gte=current_date))
                ).count()

                # Crear turno si hay disponibilidad
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
    """
    Vista que genera estadísticas de clientes:
    - Altas/bajas por mes
    - Total de clientes activos
    - Datos para gráficos
    """
    hoy = timezone.now().date()
    año_actual = hoy.year  
    año_actual = hoy.year
    
    fecha_inicio = date(año_actual, 1, 1)
    fecha_fin = date(año_actual, 12, 31)

    meses_espanol = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    
    datos = []
    for mes in range(1, 13):
        mes_inicio = date(año_actual, mes, 1)
        mes_fin = date(año_actual, mes+1, 1) if mes < 12 else date(año_actual+1, 1, 1)

        # Contar altas nuevas
        altas_nuevos = Cliente.objects.filter(
            fecha_alta__gte=mes_inicio, 
            fecha_alta__lt=mes_fin
        ).count()

        # Contar reactivaciones
        reactivaciones = Cliente.objects.filter(
            activo=True,
            modificado__gte=mes_inicio,
            modificado__lt=mes_fin,
            fecha_baja__isnull=False
        ).count()
        
        altas = altas_nuevos + reactivaciones

        # Contar bajas
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

@login_required
def resetear_estados_mensual_view(request):
    """
    Vista que ejecuta el comando para resetear estados mensuales:
    - Cambia estado a 'pendiente' el primer día de cada mes
    - Para clientes regulares con pago confirmado del mes anterior
    """
    try:
        call_command('resetear_estados_mensual', force=True, silent=False)
        messages.success(request, "Se reiniciaron los estados mensuales correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al reiniciar los estados: {str(e)}")
    
    return redirect('clientes:lista_clientes')