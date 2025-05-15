from django.db import models
from planes.models import Plan
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date

class Cliente(models.Model):
    TIPO_CHOICES = [('regular', 'Regular'), ('eventual', 'Eventual')]
    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(unique=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    dias = models.CharField(max_length=100, blank=True, null=True)
    hora = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='regular')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(default=date.today, null=False)  # Asegúrate que sea DateField
    fecha_baja = models.DateField(null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"

    def clean(self):
        if self.plan and (not self.dias or not self.hora):
            raise ValidationError("Debe asignar días y horarios para el plan seleccionado")
        
        if self.plan and self.dias and self.hora:
            dias_asignados = len(self.dias.split(','))
            horas_asignadas = len(self.hora.split(','))
            
            if dias_asignados != self.plan.cantidad_dias:
                raise ValidationError(f"El plan seleccionado requiere exactamente {self.plan.cantidad_dias} día(s)")
            
            if dias_asignados != horas_asignadas:
                raise ValidationError("Debe asignar un horario para cada día seleccionado")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)