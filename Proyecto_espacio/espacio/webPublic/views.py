from django.shortcuts import render
from empleados.models import Empleado
from eventos.models import Evento
from planes.models import Plan

def home(request):
    planes = Plan.objects.filter(mostrar_en_web=True, activo=True)
    empleados = Empleado.objects.filter(mostrar_en_web=True, activo=True).values(
    'nombre', 'instagram' , 'imagen_perfil' )
    
    return render(request, 'webPublic/home.html', {'planes': planes, 'empleados': empleados})

def eventos(request):
    eventos = Evento.objects.filter(mostrar_en_web=True, estado=True)
    return render(request, 'webPublic/eventos.html', {'eventos': eventos})
