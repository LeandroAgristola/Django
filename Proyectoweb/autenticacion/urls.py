from django.urls import path
from .views import VRegistro, cerrar_sesion, logear

urlpatterns = [
    path('',VRegistro.as_view(), name="Autenticacion"), #nos muestra la clase VRegistro como un vista
    path('cerrar_sesion',cerrar_sesion.as_view(), name="cerrar_sesion"), #nos muestra la clase cerrar sesion como un vista
    path('logear',logear.as_view(), name="logear"), #nos muestra la clase VRegistro como un vista
]


