"""
Configuración de URL para proyecto TiendaOnline.

La lista `urlpatterns` dirige las URL a las vistas. Para obtener más información, consulte:
 https://docs.djangoproject.com/en/5.0/topics/http/urls/
Ejemplos:
Vistas de funciones
 1. Agregue una importación: desde las vistas de importación de my_app
 2. Agregue una URL a urlpatterns: ruta('', views.home, nombre='home')
Vistas basadas en clases
 1. Agregue una importación: desde other_app.views import Inicio
 2. Agregue una URL a urlpatterns: ruta('', Home.as_view(), nombre='home')
Incluyendo otra URLconf
 1. Importe la función include(): desde django.urls importe include, ruta
 2. Agregue una URL a urlpatterns: ruta('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestionPedidos import views #importar el archivo views antes de registrar el path
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('busqueda_productos/', views.busqueda_productos), #registramos el path
    path('buscar/',views.buscar),
    path('contacto/',views.contacto),
]
