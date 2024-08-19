from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class VRegistro(View):
    def get(self, request):
        form=UserCreationForm()
        return render(request,"registro/registro.html",{"form":form})
    
    def post(self, request):
        form=UserCreationForm(request.POST) #guardamos el usuario y la contraseña que el Usuario introdujo en el form de registro
        if form.is_valid(): #si el formulario es valido: 
            usuario=form.save() #guardamos la informacion introducida en la base de datos (tabla auth_user)
            login(request,usuario) #automaticamente cuando se crea el usuario, se logea
            return redirect('Home') #una vez creado el usuarios, redireccionamos al home
        else:
            for msj in form.error_messages: #recorremos cada msj de error que haya en el formulario
                messages.error(request, form.error_messages[msj])
            return render(request,"registro/registro.html",{"form":form}) #mostramos el formulario con los errores 
        

def cerrar_sesion(request): #creamola funcion para cerrar sesion
    logout(request)
    return redirect('Home') #una vez cerrada la sesion, redireccionamos al home