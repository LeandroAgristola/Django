from .models import Evento
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventoForm
from django.views.decorators.http import require_POST

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
            form.save()
            return redirect('eventos_admin:lista_eventos')
        else:
            eventos = Evento.objects.filter(estado=True)
            papelera = Evento.objects.filter(estado=False)
            return render(request, 'eventos/lista_eventos.html', {
                'eventos': eventos,
                'papelera': papelera,
                'form': form,
                'mostrar_modal': True  # para que reabra el modal con los errores
            })
    else:
        return redirect('eventos_admin:lista_eventos')

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('eventos_admin:lista_eventos')
    else:
        form = EventoForm(instance=evento)

    eventos = Evento.objects.filter(estado=True)
    papelera = Evento.objects.filter(estado=False)
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'papelera': papelera,
        'form': form,
        'mostrar_modal': True
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
    evento.estado = True
    evento.save()
    return redirect('eventos_admin:lista_eventos')

@require_POST
@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.delete()
    return redirect('eventos_admin:lista_eventos')