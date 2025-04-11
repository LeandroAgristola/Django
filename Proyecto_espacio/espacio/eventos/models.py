from django.db import models
import os

class Evento(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=100)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    ubicacion = models.CharField(max_length=100, null=False, blank=False)
    cupos = models.IntegerField(default=0, null=False, blank=False)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.BooleanField(default=True)
    mostrar_en_web = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha', '-hora']
    
    def delete(self, *args, **kwargs):
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d/%m/%Y')}"
