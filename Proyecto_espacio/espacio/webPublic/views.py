from django.shortcuts import render
from empleados.models import Empleado
from eventos.models import Evento

def home(request):
        planes = [
        {"nombre": "Plan A", "detalle": "Una vez por semana", "precio": "25000"},
        {"nombre": "Plan B", "detalle": "Dos veces por semana", "precio": "30000"},
        {"nombre": "Plan C", "detalle": "Tres veces por semana", "precio": "45000"},
        {"nombre": "Plan D", "detalle": "Cuatro veces por semana", "precio": "60000"},
        {"nombre": "Plan Full", "detalle": "Cinco veces por semanaa", "precio": "65000"},
        {"nombre": "Personalizado", "detalle": "Dos veces por semana", "precio": "70000"},
    ]
        empleados = Empleado.objects.filter(mostrar_en_web=True, activo=True).values(
        'nombre', 'instagram' , 'imagen_perfil' )
    
        return render(request, 'webPublic/home.html', {'planes': planes, 'empleados': empleados})

def eventos(request):
    eventos = Evento.objects.filter(mostrar_en_web=True, estado=True).values(
        'titulo', 'fecha' ,'descripcion' , 'hora' , 'ubicacion', 'precio', 'cupos', 'imagen', 'pago_enlace', 'link_pago')

    return render(request, 'webPublic/eventos.html', {'eventos': eventos})
