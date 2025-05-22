from django.db import models
from clientes.models import Cliente


class Turno(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')

    class Meta:
        unique_together = ('fecha', 'hora', 'cliente')  # evita duplicados
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.fecha} - {self.hora} - {self.cliente}"
