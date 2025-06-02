from django.db import models
from clientes.models import Cliente


class Turno(models.Model):
    """
    Modelo que representa un turno en el sistema.
    - Relacionado con un cliente mediante ForeignKey
    - Validación para evitar duplicados con unique_together
    - Ordenamiento natural por fecha y hora
    """
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')

    class Meta:
        unique_together = ('fecha', 'hora', 'cliente')  #  Evita turnos duplicados para mismo cliente
        ordering = ['fecha', 'hora'] # Ordenamiento por defecto

    def __str__(self):
        return f"{self.fecha} - {self.hora} - {self.cliente}"
