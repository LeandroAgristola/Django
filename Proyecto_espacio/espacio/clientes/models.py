from django.db import models
from planes.models import Plan

class Cliente(models.Model):
    TIPO_CHOICES = [('regular', 'Regular'), ('eventual', 'Eventual')]
    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(unique=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    dias = models.CharField(max_length=100, blank=True, null=True)  # futuro: lista de días
    hora = models.CharField(max_length=100, blank=True, null=True)  # futuro: desde calendario
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"