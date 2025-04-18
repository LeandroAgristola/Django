from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Configuracion
from .forms import ConfiguracionForm
from django.contrib.auth.decorators import login_required

@require_POST
@login_required
def actualizar_campo(request, campo):
    configuracion = Configuracion.objects.first()
    nuevo_valor = request.POST.get("valor", "").strip()

    if hasattr(configuracion, campo):
        setattr(configuracion, campo, nuevo_valor)
        configuracion.save()
    
    return redirect('panel_configuracion')

@login_required
def panel_configuracion(request):
    configuracion, created = Configuracion.objects.get_or_create(id=1)
    campos = {
        'nombre_estudio': configuracion.nombre_estudio,
        'direccion': configuracion.direccion,
        'telefono': configuracion.telefono,
        'email': configuracion.email,
        'instagram': configuracion.instagram,
        'facebook': configuracion.facebook,
        'youtube': configuracion.youtube,
        'whatsapp': configuracion.whatsapp,
        'horario_semana': configuracion.horario_semana,
        'horario_sabado': configuracion.horario_sabado,
    }

    iconos = {
        'nombre_estudio': 'building',
        'direccion': 'location-dot',
        'telefono': 'phone',
        'email': 'envelope',
        'instagram': 'instagram',
        'facebook': 'facebook',
        'youtube': 'youtube',
        'whatsapp': 'whatsapp',
        'horario_semana': 'clock',
        'horario_sabado': 'clock',
    }

    return render(request, 'configuracion/panel_configuracion.html', {
        'configuracion': campos,
        'iconos': iconos
    })