from django.urls import path
from . import views

app_name = 'eventos_admin'

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('<int:pk>/', views.detalle_eventos, name='detalle_eventos'),
    path('nuevo/', views.crear_evento, name='crear_evento'), 
    path('<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/<int:pk>/desactivar/', views.desactivar_evento, name='desactivar_evento'),
    path('eventos/<int:pk>/reactivar/', views.reactivar_evento, name='reactivar_evento'),
    path('inscribir/<int:evento_id>/', views.inscribir_cliente, name='inscribir_cliente'),
    path('confirmar-pago/<int:inscripcion_id>/', views.confirmar_pago_evento, name='confirmar_pago_evento'),
    path('eliminar-inscripcion/<int:inscripcion_id>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('exportar-inscriptos/<int:evento_id>/', views.exportar_inscriptos_pdf, name='exportar_inscriptos_pdf'),
    path('estadisticas/', views.estadisticas_eventos, name='estadisticas_eventos'),

]