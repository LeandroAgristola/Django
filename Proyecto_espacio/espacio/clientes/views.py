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

            fecha_str = request.POST.get('fecha_alta')
            if fecha_str:
                try:
                    # Convertimos string a datetime (a las 00:00 hs)
                    cliente.fecha_alta = datetime.strptime(fecha_str, "%Y-%m-%d")
                except ValueError:
                    cliente.fecha_alta = datetime.today()
            else:
                cliente.fecha_alta = datetime.today()

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
        form = ClienteForm(instance=cliente)

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
        # Solo preparamos el cliente para reactivación pero NO lo guardamos
        cliente.activo = True
        fecha_str = request.POST.get('fecha_alta')
        cliente.fecha_alta = datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str else datetime.today()
        cliente.estado = 'pendiente'
        cliente.plan = None
        cliente.save()
        
        # Redirigir a la vista de edición con los datos precargados
        form = ClienteForm(instance=cliente)
        return render(request, 'clientes/forms_cliente.html', {
            'form': form,
            'reactivando': True,  # Flag para identificar que viene de una reactivación
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
    print("TIPO DE USUARIO:", type(request.user))
    print("ATRIBUTOS:", dir(request.user))
    plan_id = request.GET.get('plan_id') or request.POST.get('plan_id')
    configuracion = Configuracion.objects.first()
    dias_habilitados = configuracion.dias_habilitados if configuracion else []

    if not plan_id:
        messages.error(request, "No se especificó ningún plan")
        return redirect('clientes:crear_cliente')

    plan = Plan.objects.get(id=plan_id)
    config = Configuracion.objects.first()

    if request.method == 'POST':
        dias = request.POST.getlist('dias[]')
        horas = request.POST.getlist('horas[]')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        mail = request.POST.get('mail')
        estado = request.POST.get('estado')

        fecha_str = request.GET.get('fecha_alta') or request.POST.get('fecha_alta')
        try:
            fecha_alta = datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str else datetime.today()
        except ValueError:
            fecha_alta = datetime.today()

        if not dias or not horas:
            messages.error(request, "Debés seleccionar días y horarios.")
            return redirect(request.path + f"?plan_id={plan_id}")

        cliente, creado = Cliente.objects.get_or_create(
            mail=mail,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'dni': dni,
                'telefono': telefono,
                'plan': plan,
                'dias': ", ".join(dias),
                'hora': ", ".join(horas),
                'tipo': 'regular',
                'estado': estado,
                'fecha_alta': fecha_alta
            }
        )

        if not creado:
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.dni = dni
            cliente.telefono = telefono
            cliente.plan = plan
            cliente.dias = ", ".join(dias)
            cliente.hora = ", ".join(horas)
            cliente.tipo = 'regular'
            cliente.estado = estado
            cliente.fecha_alta = fecha_alta
            cliente.save()
            cliente.turnos.all().delete()
            
        generar_turnos_futuros(cliente)

        messages.success(request, "Cliente y turnos asignados correctamente.")
        return redirect('clientes:lista_clientes')

    return render(request, 'clientes/asignar_turnos.html', {
        'plan': plan,
        'config': config,
        'dias_semana': dias_habilitados,
        'dias_semana_json': json.dumps(dias_habilitados),
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

@login_required(login_url='login')
def clientes_estadisticas(request):
    rango = request.GET.get('rango', '1m')
    hoy = datetime.now()

    if rango == '3m':
        desde = hoy - timedelta(days=90)
    elif rango == '1y':
        desde = hoy - timedelta(days=365)
    else:
        desde = hoy - timedelta(days=30)

    altas = Cliente.objects.filter(fecha_alta__gte=desde).count()
    bajas = Cliente.objects.filter(fecha_baja__gte=desde).count()
    total_activos = Cliente.objects.filter(activo=True).count()

    return JsonResponse({
        'altas': altas,
        'bajas': bajas,
        'total_activos': total_activos,
        'total_periodo': altas + bajas
    })