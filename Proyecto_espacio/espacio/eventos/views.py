from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import EventoForm, InscripcionForm
from .models import Evento, InscripcionEvento

@login_required
def lista_eventos(request):
    eventos = Evento.objects.filter(estado=True)
    papelera = Evento.objects.filter(estado=False)
    form = EventoForm()  # Agregá esto
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'papelera': papelera,
        'form': form,  # Y esto
    })

@login_required
def detalle_eventos(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_eventos.html', {'evento': evento})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            new_fecha = form.cleaned_data.get('fecha')
            new_hora = form.cleaned_data.get('hora')
            new_datetime = datetime.combine(new_fecha, new_hora)
            now = datetime.now().replace(second=0, microsecond=0)
            if new_datetime < now:
                form.add_error('fecha', "La fecha y hora deben ser posteriores a la actual.")
                return render(request, 'eventos/evento_form.html', {'form': form})
            form.save()
            return redirect('eventos_admin:lista_eventos')
        else:
            print(form.errors)  # Esto te ayudará a ver qué validación falla
            return render(request, 'eventos/evento_form.html', {'form': form})
    else:
        form = EventoForm()
        return render(request, 'eventos/evento_form.html', {'form': form})
    
@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            new_fecha = form.cleaned_data.get('fecha')
            new_hora = form.cleaned_data.get('hora')
            new_datetime = datetime.combine(new_fecha, new_hora)
            now = datetime.now().replace(second=0, microsecond=0)
            original_datetime = datetime.combine(evento.fecha, evento.hora)
            # Si se modificó la fecha/hora, se valida que no sea en el pasado
            if (new_datetime != original_datetime) and (new_datetime < now):
                form.add_error('fecha', "La fecha y hora deben ser posteriores a la actual.")
                return render(request, 'eventos/evento_form.html', {'form': form})
            form.save()
            return redirect('eventos_admin:lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/evento_form.html', {'form': form})

@require_POST
@login_required
def desactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    # Contar inscripciones actuales
    inscripciones = InscripcionEvento.objects.filter(evento=evento)
    cantidad_inscripciones = inscripciones.count()

    # Restaurar cupos al original sumando inscripciones eliminadas
    evento.cupos += cantidad_inscripciones

    # Eliminar inscripciones
    inscripciones.delete()

    # Cambiar estado
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
def inscribir_cliente(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    clientes_regulares = [
        {'nombre': 'Ana Gómez', 'email': 'ana@example.com', 'telefono': '123456789'},
        {'nombre': 'Carlos Pérez', 'email': 'carlos@example.com', 'telefono': '987654321'},
        {'nombre': 'Lucía Martínez', 'email': 'lucia@example.com', 'telefono': '111222333'},
    ]  # Simulación de clientes, deberías obtenerlos de tu base de datos
    #clientes = Cliente.objects.all().values_list('id', 'nombre')

    if request.method == 'POST':    
        if evento.cupos <= 0:
            messages.error(request, "No hay cupos disponibles para este evento.")
            return redirect('eventos_admin:inscribir_cliente', pk=pk)
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.evento = evento
            inscripcion.save()
            evento.cupos -= 1
            evento.save()
            return redirect('eventos_admin:detalle_eventos', pk=pk)
    else:
        form = InscripcionForm()

    return render(request, 'eventos/inscribir_cliente.html', {
        'form': form,
        'evento': evento,
        'clientes': clientes_regulares
    })

@require_POST
@login_required
def eliminar_inscripcion(request, insc_id):
    inscripcion = get_object_or_404(InscripcionEvento, id=insc_id)
    evento = inscripcion.evento
    inscripcion.delete()
    evento.cupos += 1
    evento.save()
    return redirect('eventos_admin:detalle_eventos', pk=evento.pk)

@require_POST
@login_required
def confirmar_pago(request, insc_id):
    inscripcion = get_object_or_404(InscripcionEvento, id=insc_id)
    # Se muestra el botón de confirmar solo para inscripciones pendientes y eventos pagados.
    if inscripcion.estado == 'pendiente' and inscripcion.evento.precio > 0:
         inscripcion.estado = 'confirmado'
         inscripcion.save()
         messages.success(request, "Pago confirmado.")
    else:
         messages.info(request, "No es necesario confirmar este pago.")
    return redirect('eventos_admin:detalle_eventos', pk=inscripcion.evento.pk)