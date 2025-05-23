from django.db import models
from planes.models import Plan
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from datetime import date, datetime

class Cliente(models.Model):

    """
    Modelo que representa un cliente del estudio.
    - Relacionado con un Plan mediante ForeignKey
    - Maneja diferentes estados y tipos de clientes
    - Incluye validaciones para días y horarios asignados
    - Calcula propiedades relacionadas con pagos
    """

    # Opciones para campos de selección
    TIPO_CHOICES = [('regular', 'Regular'), ('eventual', 'Eventual')]
    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]

    # Campos principales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True) # DNI como identificador único
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(unique=True)  # Email como identificador único

    # Relación con Plan
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True) 

    # Campos para turnos
    dias = models.CharField(max_length=100, blank=True, null=True) # Días asignados (ej: "lunes,miercoles")
    hora = models.CharField(max_length=100, blank=True, null=True) # Horarios asignados (ej: "10:00,14:00")

    # Estado y tipo
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='regular')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # Campos de control
    activo = models.BooleanField(default=True)   # Indica si el cliente está activo
    fecha_alta = models.DateField(default=date.today, null=False) # Fecha de registro
    fecha_baja = models.DateField(null=True, blank=True) # Fecha de baja (si aplica)
    modificado = models.DateTimeField(auto_now=True) # Última modificación
    ultima_confirmacion = models.DateField(null=True, blank=True) # Último pago confirmado

    def __str__(self):
        """Representación legible del cliente"""
        return f"{self.nombre} {self.apellido} ({self.dni})"

    def clean(self):
        """
        Validación personalizada:
        - Verifica que los días/horarios coincidan con el plan
        - Valida cantidad de días según plan
        - Valida que haya un horario por cada día
        """

        if self.plan and (not self.dias or not self.hora):
            raise ValidationError("Debe asignar días y horarios para el plan seleccionado")
        
        if self.plan and self.dias and self.hora:
            dias_asignados = len(self.dias.split(','))
            horas_asignadas = len(self.hora.split(','))
            
            if dias_asignados != self.plan.cantidad_dias:
                raise ValidationError(f"El plan seleccionado requiere exactamente {self.plan.cantidad_dias} día(s)")
            
            if dias_asignados != horas_asignadas:
                raise ValidationError("Debe asignar un horario para cada día seleccionado")
    @property
    def cuota_vencida(self):
        """
        Propiedad que calcula si la cuota está vencida:
        - Considera día 7 como límite
        - Verifica estado pendiente
        - Compara mes/año de última confirmación
        """
        hoy = timezone.now().date()
        if not self.ultima_confirmacion:
            return hoy.day > 7 and self.estado == 'pendiente'
        
        return (hoy.day > 7 and 
                self.estado == 'pendiente' and
                (self.ultima_confirmacion.month < hoy.month or 
                self.ultima_confirmacion.year < hoy.year))
        
    @property
    def mes_pagado(self):
        """Verifica si el cliente ha pagado el mes actual"""
        if not self.ultima_confirmacion:
            return False
            
        hoy = timezone.now().date()
        return (self.estado == 'confirmado' and 
                self.ultima_confirmacion.month == hoy.month and 
                self.ultima_confirmacion.year == hoy.year)
    
    @property
    def mostrar_estado_pago(self):
        """
        Retorna información de estado de pago para mostrar en UI:
        - Texto descriptivo
        - Clase CSS para estilizar
        """
        if self.tipo == 'eventual':
            return None # No aplica para clientes eventuales
        hoy = timezone.now().date()
        
        if not self.ultima_confirmacion:
            return {
                'texto': 'Pendiente',
                'clase': 'bg-warning'
            }
        
        # Pago confirmado para el mes actual
        if self.estado == 'confirmado' and \
        self.ultima_confirmacion.month == hoy.month and \
        self.ultima_confirmacion.year == hoy.year:
            return {
                'texto': 'Pagado',
                'clase': 'bg-success'
            }
        # Pago vencido (pasó el día 7 y está pendiente)
        if hoy.day > 7 and self.estado == 'pendiente':
            return {
                'texto': 'Vencido',
                'clase': 'bg-danger'
            }
        # Estado por defecto
        return {
            'texto': 'Pendiente',
            'clase': 'bg-secondary'
        }