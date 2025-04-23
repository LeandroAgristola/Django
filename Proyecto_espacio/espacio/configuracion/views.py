from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Configuracion
from .forms import ConfiguracionForm
from django.contrib.auth.decorators import login_required

@login_required
def panel_config(request):
    configuracion = Configuracion.objects.first()
    return render(request, "configuracion/panel_config.html", {"configuracion": configuracion})

@login_required
def editar_datos(request):
    configuracion = Configuracion.objects.first()
    if not configuracion:
        configuracion = Configuracion.objects.create()

    if request.method == "POST":
        form = ConfiguracionForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            return redirect("configuracion:panel_config")
    else:
        form = ConfiguracionForm(instance=configuracion)

    return render(request, "configuracion/forms_config.html", {"form": form})