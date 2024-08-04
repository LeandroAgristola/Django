from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):

    return render(request,"ProyectowebApp/home.html")

def tienda(request):

    return render(request,"ProyectowebApp/tienda.html")



