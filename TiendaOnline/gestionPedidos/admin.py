from django.contrib import admin

from gestionPedidos.models import Clientes, Articulos, Pedidos  #importamos la tabla q queremos agregar al administrador web

# Register your models here.

class ClientesAdmin(admin.ModelAdmin):
    list_display=("nombre","direccion","telefono") #Muestra estos campos en los listados en administracion
    search_fields=("nombre","telefono") #Habilitamos el panel de busqueda segun esos dos campos 

class ArticulosAdmin(admin.ModelAdmin):
    list_display=("nombre","seccion","precio")
    search_fields=("nombre","precio")
    list_filter=("seccion",) #al final de las comillas colocar una "," por es una tubla

admin.site.register(Clientes, ClientesAdmin) #registramos la tabla para administrar
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(Pedidos)