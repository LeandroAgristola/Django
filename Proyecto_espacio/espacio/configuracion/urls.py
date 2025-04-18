from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel_configuracion, name='panel_configuracion'),
    path('actualizar/<str:campo>/', views.actualizar_campo, name='actualizar_campo'),
]