from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from carro.carro import Carro
from pedidos.models import LineaPedidos, Pedido
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


# Create your views here.

@login_required(login_url="/autenticacion/logear")
def procesar_pedido(request):
    pedido=pedido.objects.create(user=request.user)
    carro=Carro(request)
    lineas_pedido=list()
    for key,  value in carro.carro.items():
        lineas_pedido.append(LineaPedidos(
            
            producto_id=key,
            cantidad=value["cantidad"],
            user=request.user,
            pedido=pedido,
            
        ))
    
    LineaPedidos.objects.bulk_create(lineas_pedido)

    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.username,
        emailusuario=request.usermail
    )

    messages.succes(request, "El pedido se ha creado correctamente")

    return redirect("../tienda")

def enviar_mail(**kwargs):
    asunto="Gracias por tu pedido"
    mensaje=render_to_string("emails/pedidos.html",{
        "pedido":kwargs.get("pedido"),
        "lineas_pedidos":kwargs.get("lineas_pedido"),
        "nombreusuario":kwargs.get("nombreusuario")


    })

    mensaje_texto=strip_tags(mensaje)
    from_email="tienda@email.com"
    to=kwargs.get("emailusuario")

    send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje) 
