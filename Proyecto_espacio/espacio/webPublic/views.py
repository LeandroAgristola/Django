from django.shortcuts import render

def home(request):
        planes = [
        {"nombre": "Plan A", "detalle": "Una vez por semana", "precio": "25000"},
        {"nombre": "Plan B", "detalle": "Dos veces por semana", "precio": "30000"},
        {"nombre": "Plan C", "detalle": "Tres veces por semana", "precio": "45000"},
        {"nombre": "Plan D", "detalle": "Cuatro veces por semana", "precio": "60000"},
        {"nombre": "Plan Full", "detalle": "Cinco veces por semanaa", "precio": "65000"},
        {"nombre": "Personalizado", "detalle": "Dos veces por semana", "precio": "70000"},
    ]
        empleados = [
        {"nombre": "Juan", "instagram": "juan", "imagen": "imgEmpleados/perfil01.png"},
        {"nombre": "Martin", "instagram": "martin", "imagen": "imgEmpleados/perfil02.png"},
        {"nombre": "Mariana", "instagram": "mariana", "imagen": "imgEmpleados/perfil03.png"},
        {"nombre": "Estefania", "instagram": "estefania", "imagen": "imgEmpleados/perfil04.png"},
    ]
        return render(request, 'webPublic/home.html', {'planes': planes, 'empleados': empleados})

def eventos(request):
    eventos = [
        {
            "nombre": "Clase",
            "fecha": "10/03/2025",
            "hora": "10:00 hs",
            "ubicacion": "Estudio",
            "costo": "0",
            "cupos_disponibles": 20,
            "imagen": "imgEventos/ImgEvento01.png"
        },
        {
            "nombre": "Clase",
            "fecha": "10/05/2025",
            "hora": "10:00 hs",
            "ubicacion": "Estudio",
            "costo": "25000",
            "cupos_disponibles": 20,
            "imagen": "imgEventos/ImgEvento02.png"
        },
        {
            "nombre": "Clase",
            "fecha": "10/08/2025",
            "hora": "09:00 hs",
            "ubicacion": "Estudio",
            "costo": "18000",
            "cupos_disponibles": 20,
            "imagen": "imgEventos/ImgEvento03.png"
        },
        {
            "nombre": "Clase",
            "fecha": "10/10/2025",
            "hora": "18:00 hs",
            "ubicacion": "Estudio",
            "costo": "35000",
            "cupos_disponibles": 0,
            "imagen": "imgEventos/ImgEvento04.png"
        },	
    ]
    return render(request, 'webPublic/eventos.html', {'eventos': eventos})
