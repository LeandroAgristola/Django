from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto

# Create your views here.

def busqueda_productos(request):
    return render(request, "busqueda_productos.html")

def buscar(request):

    if request.GET["productos"]:
    
        prd=request.GET["productos"] 

        if len(prd)>20: # si el texto ingresado en mayor a 20 caracteres mostramos el msj de error 
            mensaje="Texto demasiado largo"
        else:
            articulos=Articulos.objects.filter(nombre__icontains=prd) #icontains realiza un "like" de sql buscando lo introducido en prd en la base de datos
            return render(request,"resultados_busqueda.html", {"articulos":articulos,"query":prd})
        
    else:
        mensaje="Intrudice un articulo"
    
    return HttpResponse(mensaje)

def contacto(request):

    if request.method=="POST":

        miFormulario=FormularioContacto(request.POST) #instaciamos el objeto 

        if miFormulario.is_valid():

            infoForm=miFormulario.cleaned_data

            send_mail(infoForm['asunto'],infoForm['mensaje'],infoForm.get('email',''),['leopoldaso007@gmail.com'],)

            return render(request,"Gracias.html")
        
    else: 

        miFormulario=FormularioContacto() #Esta instruccion hace q cuando entremos al formulario se encuentre vacio

    return render(request,"Formulario_Contacto.html",{"form":miFormulario})


# def contacto(request):

#     if request.method=="POST":

#         subject=request.POST["asunto"] # rescatamos el campo de asunto del template "contacto"

#         message=request.POST["mensaje"] + " "  + request.POST["email"] # rescatamos el campo de mensaje y email del template "contacto"

#         email_from=settings.EMAIL_HOST_USER 

#         recipient_list=["direccion de correo electronico"] # Especificamos a que direccion enviar el formulario de contacto

#         send_mail(subject,message,email_from,recipient_list)

#         return render(request,"gracias.html")

#     return render(request,"contacto.html")