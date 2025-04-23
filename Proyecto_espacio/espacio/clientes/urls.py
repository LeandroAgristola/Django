from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('asignar-turnos/', views.asignar_turnos, name='asignar_turnos'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('desactivar/<int:cliente_id>/', views.desactivar_cliente, name='desactivar_cliente'),
    path('reactivar/<int:cliente_id>/', views.reactivar_cliente, name='reactivar_cliente'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('confirmar_pago/<int:cliente_id>/', views.confirmar_pago, name='confirmar_pago'),
]