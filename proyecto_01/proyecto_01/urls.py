"""
URL configuration for proyecto_01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from proyecto_01.views import saludo, obtenerFecha, calculaEdad, contenido#importamos lso modulos de nuestro archivo "views"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', saludo), #agregamos la URL URL par saludo
    path('fecha/', obtenerFecha), #agregamos la URL para obtenerFecha
    path('edades/<int:edad>/<int:agno>/', calculaEdad), #establecemos el parametro que vamos a pasar y los pasamos a entero con int
    path('contenido/',contenido)
]
