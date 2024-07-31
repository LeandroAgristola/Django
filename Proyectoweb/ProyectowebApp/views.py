from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):

    return render(request,"ProyectowebApp/home.html")

def tienda(request):

    return render(request,"ProyectowebApp/tienda.html")

def blog(request):

    return render(request,"ProyectowebApp/blog.html")

def contacto(request):

    return render(request,"ProyectowebApp/contacto.html")

