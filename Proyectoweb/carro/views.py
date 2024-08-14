from django.shortcuts import render
from .carro import Carro
from tienda.models import Producto
from django.shortcuts import redirect

# Create your views here.

def agragar_producto(request, producto_id):
    carro=carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect("tienda")

def eliminar_producto(request, producto_id):
    carro=carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("tienda")
