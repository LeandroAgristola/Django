from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Plan
from calendario.models import Turno
from planes.models import Plan
from configuracion.models import Configuracion
from .forms import ClienteForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta, date
from django.contrib import messages
import json
from django.http import JsonResponse

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

    planes = Plan.objects.all()

    return render(request, 'clientes/lista_clientes.html', {
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
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
    cliente = None

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.tipo = 'regular'
            
            # Manejar fecha de alta
            fecha_str = request.POST.get('fecha_alta')
            if fecha_str:
                try:
                    cliente.fecha_alta = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except ValueError:
                    cliente.fecha_alta = date.today()
            else:
                cliente.fecha_alta = date.today()
                
            cliente.save()
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/forms_cliente.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista_clientes')
    else:
        # Asegurar que la fecha de alta se mantenga en el formulario
        initial_data = {'fecha_alta': cliente.fecha_alta.strftime("%Y-%m-%d")} if cliente.fecha_alta else {}
        form = ClienteForm(instance=cliente, initial=initial_data)

    return render(request, 'clientes/forms_cliente.html', {'form': form, 'editando': True})

@login_required
def desactivar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        fecha_baja = request.POST.get('fecha_baja')
        cliente.activo = False
        cliente.estado = 'pendiente'
        cliente.fecha_baja = fecha_baja
        cliente.save()

        # 👉 Eliminar turnos a partir de hoy
        cliente.turnos.filter(fecha__gte=date.today()).delete()

        return redirect('clientes:lista_clientes')
    return redirect('clientes:lista_clientes')

@login_required
def reactivar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.activo = True
        cliente.fecha_baja = None
        cliente.save()
        
        # Pasar la fecha existente al formulario
        initial_data = {'fecha_alta': cliente.fecha_alta.strftime("%Y-%m-%d")} if cliente.fecha_alta else {}
        form = ClienteForm(instance=cliente, initial=initial_data)
        
        return render(request, 'clientes/forms_cliente.html', {
            'form': form,
            'reactivando': True,
            'cliente_id': cliente.id
        })
    
    return redirect('clientes:lista_clientes')

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

    # Obtener datos del cliente del request
    cliente_data = {
        'nombre': request.GET.get('nombre'),
        'apellido': request.GET.get('apellido'),
        'dni': request.GET.get('dni'),
        'telefono': request.GET.get('telefono'),
        'mail': request.GET.get('mail'),
        'estado': request.GET.get('estado', 'pendiente'),
        'fecha_alta': request.GET.get('fecha_alta')
    }

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
    dias_seleccionados = cliente.dias.split(", ")
    horas_seleccionadas = cliente.hora.split(", ")
    fecha_actual = cliente.fecha_alta or date.today()
    fecha_limite = fecha_actual + timedelta(days=180)

    dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

    while fecha_actual <= fecha_limite:
        dia_en_espanol = dias_esp[fecha_actual.weekday()]

        if dia_en_espanol in dias_seleccionados:
            for hora in horas_seleccionadas:
                hora_dt = datetime.strptime(hora, "%H:%M").time()

                # Verificar si ya existe el turno
                if not Turno.objects.filter(fecha=fecha_actual, hora=hora_dt, cliente=cliente).exists():
                    Turno.objects.create(fecha=fecha_actual, hora=hora_dt, cliente=cliente)

        fecha_actual += timedelta(days=1)

@login_required
def clientes_estadisticas(request):
    hoy = timezone.now().date()
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
            Q(fecha_baja__gte=mes_inicio, fecha_baja__lt=mes_fin) |
            Q(activo=False, modificado__gte=mes_inicio, modificado__lt=mes_fin)
        ).distinct().count()
        
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