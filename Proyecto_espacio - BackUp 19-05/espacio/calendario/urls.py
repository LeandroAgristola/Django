from django.urls import path
from . import views

app_name = 'calendario'

urlpatterns = [
    path('', views.vista_calendario, name='vista_calendario'),
    path('disponibilidad/', views.disponibilidad_por_dia, name='disponibilidad_por_dia'),
    path('horarios/', views.horarios_por_dia, name='horarios_por_dia'),
    path('detalle/', views.detalle_dia, name='detalle_dia'),
    path('estadisticas/', views.estadisticas_turnos, name='estadisticas_turnos'),
]