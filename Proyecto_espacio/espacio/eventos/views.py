from .models import Evento
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventoForm
from django.views.decorators.http import require_POST

@login_required
def lista_eventos(request):
    activos = Evento.objects.filter(estado=True, fecha__gte=date.today()).order_by('fecha', 'hora')
    papelera = Evento.objects.filter(estado=False, fecha__gte=date.today()).order_by('fecha', 'hora')
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': activos,
        'papelera': papelera,
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
            return redirect('lista_eventos')
    else:
        form = EventoForm()

    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'form': form,
        'mostrar_modal': True
    })

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)

    eventos = evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'form': form,
        'mostrar_modal': True
    })

@require_POST
@login_required
def desactivar_evento(request, pk):
    evento = get_object_or_404(evento, pk=pk)
    fecha_baja = request.POST.get('fecha_baja')

    if fecha_baja:
        evento.fecha_baja = fecha_baja
        evento.activo = False
        evento.save()
    return redirect('lista_eventos')

@require_POST
@login_required
def reactivar_evento(request, pk):
    evento = get_object_or_404(evento, pk=pk)
    fecha_alta = request.POST.get('fecha_alta')

    if fecha_alta:
        evento.fecha_alta = fecha_alta
        evento.fecha_baja = None
        evento.activo = True
        evento.save()
    return redirect('lista_eventos')

@require_POST
@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(evento, pk=pk)
    evento.delete()
    return redirect('lista_eventos')