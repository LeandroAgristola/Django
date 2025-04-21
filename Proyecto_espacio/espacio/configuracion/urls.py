from django.urls import path
from . import views

app_name = "configuracion"

urlpatterns = [
    path("panel/", views.panel_config, name="panel_config"),
    path("editar/", views.editar_datos, name="editar_datos"),
]