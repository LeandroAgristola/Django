from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import EventoForm, InscribirClienteForm
from .models import InscripcionEvento, Evento
from clientes.models import Cliente

@login_required
def lista_eventos(request):
    eventos = Evento.objects.filter(estado=True)
    papelera = Evento.objects.filter(estado=False)
    form = EventoForm()
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'papelera': papelera,
        'form': form,
    })

@login_required
def detalle_eventos(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_eventos.html', {'evento': evento})

@login_required
def detalle_eventos(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_eventos.html', {'evento': evento})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento creado correctamente.")
            return redirect('eventos_admin:lista_eventos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = EventoForm()

    return render(request, 'eventos/evento_form.html', {'form': form})


@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente.")
            return redirect('eventos_admin:lista_eventos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/evento_form.html', {
        'form': form,
        'evento': evento
    })

@require_POST
@login_required
def desactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.estado = False
    evento.save()
    return redirect('eventos_admin:lista_eventos')

@require_POST
@login_required
def reactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    new_fecha_str = request.POST.get('fecha_alta')
    new_hora_str = request.POST.get('hora_alta')

    try:
        new_fecha = datetime.strptime(new_fecha_str, '%Y-%m-%d').date()
        new_hora = datetime.strptime(new_hora_str, '%H:%M').time()
    except ValueError:
        messages.error(request, "Formato de fecha u hora incorrecto.")
        return redirect('eventos_admin:lista_eventos')

    nueva_fecha_hora = datetime.combine(new_fecha, new_hora)
    actual_fecha_hora = datetime.combine(evento.fecha, evento.hora)
    ahora = datetime.now().replace(second=0, microsecond=0)

    if nueva_fecha_hora == actual_fecha_hora:
        messages.error(request, "La nueva fecha y hora deben ser distintas a la actual.")
        return redirect('eventos_admin:lista_eventos')

    if nueva_fecha_hora < ahora:
        messages.error(request, "La nueva fecha y hora no pueden ser anteriores al momento actual.")
        return redirect('eventos_admin:lista_eventos')

    evento.fecha = new_fecha
    evento.hora = new_hora
    evento.estado = True
    evento.save()
    return redirect('eventos_admin:lista_eventos')

@require_POST
@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.delete()
    return redirect('eventos_admin:lista_eventos')

@login_required
def inscribir_cliente(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        form = InscribirClienteForm(request.POST)
        if form.is_valid():
            tipo_cliente = form.cleaned_data['tipo_cliente']
            estado = form.cleaned_data['estado']

            if tipo_cliente == 'cargado':
                email = request.POST.get('cliente_id')
                cliente = Cliente.objects.get(mail=email)

            else:  # nuevo
                cliente = Cliente.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    apellido=form.cleaned_data['apellido'],
                    dni=int(datetime.now().timestamp()),  # temporal, o generá uno por formulario
                    mail=form.cleaned_data['email'],
                    plan=None,
                    tipo='eventual',
                    estado=estado,
                    activo=True,
                )

            inscripcion = InscripcionEvento.objects.create(
                evento=evento,
                nombre=cliente.nombre,
                apellido=cliente.apellido,
                email=cliente.mail,
                telefono=form.cleaned_data['telefono'],
                estado=estado,
                cliente=cliente
            )

            messages.success(request, "Cliente inscrito correctamente.")
            return redirect('eventos_admin:detalle_eventos', pk=evento.id)
        else:
            messages.error(request, "Error al inscribir cliente.")
    else:
        form = InscribirClienteForm()

    return render(request, 'eventos/inscribir_cliente.html', {
        'form': form,
        'evento': evento,
        'clientes': clientes
    })