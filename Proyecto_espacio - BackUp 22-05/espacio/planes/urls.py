from django.urls import path
from . import views

app_name = 'planes'

urlpatterns = [
    path('', views.listado_planes, name='lista_planes'),
    path('crear/', views.crear_plan, name='crear_plan'),
    path('editar/<int:pk>/', views.editar_plan, name='editar_plan'),
    path('desactivar/<int:pk>/', views.desactivar_plan, name='desactivar_plan'),
    path('reactivar/<int:pk>/', views.reactivar_plan, name='reactivar_plan'),
    path('eliminar/<int:pk>/', views.eliminar_plan, name='eliminar_plan'),
    path('estadisticas/', views.estadisticas_planes, name='estadisticas_planes'),
]