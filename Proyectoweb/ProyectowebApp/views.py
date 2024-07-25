from django.shortcuts import render, HttpResponse
from servicios.models import Servicio #importamos el servicio del models de la APP servicios para poder trabajar sobre la vista servicios

# Create your views here.

def home(request):

    return render(request,"ProyectowebApp/home.html")

def servicios(request):

    servicios=Servicio.objects.all()# le deciamos a django que importe todos los servicios que creamos 
    return render(request,"ProyectowebApp/servicios.html",{"servicios":servicios})

def tienda(request):

    return render(request,"ProyectowebApp/tienda.html")

def blog(request):

    return render(request,"ProyectowebApp/blog.html")

def contacto(request):

    return render(request,"ProyectowebApp/contacto.html")

