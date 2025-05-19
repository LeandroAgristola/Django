from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_empleados, name='lista_empleados'),
    path('<int:pk>/', views.detalle_empleado, name='detalle_empleado'),
    path('nuevo/', views.crear_empleado, name='crear_empleado'),
    path('<int:pk>/editar/', views.editar_empleado, name='editar_empleado'),
    path('<int:pk>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
    path('empleados/<int:pk>/desactivar/', views.desactivar_empleado, name='desactivar_empleado'),
    path('empleados/<int:pk>/reactivar/', views.reactivar_empleado, name='reactivar_empleado'),
]