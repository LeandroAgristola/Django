from django.db import models
import os
from django.core.exceptions import ValidationError
from clientes.models import Cliente

class Evento(models.Model):
    titulo = models.TextField(max_length=50)
    descripcion = models.TextField(max_length=100)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    ubicacion = models.CharField(max_length=100, null=False, blank=False)
    cupos = models.IntegerField(default=0, null=False, blank=False)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    mostrar_en_web = models.BooleanField(default=False)
    pago_enlace = models.URLField(blank=True, null=True)
    pago_en_estudio = models.BooleanField(default=False)
    link_pago = models.URLField(blank=True, null=True)

    #Establecemos un formateo en el precio para mostrarlo en la web ejemplo: 1.000,00
    @property
    def precio_formateado(self):
        return f"{self.precio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha', '-hora']

    # Validación para asegurarse de que la imagen sea un archivo de imagen
    def clean(self):
        super().clean()
        # Solo validar métodos de pago si el evento tiene costo mayor a 0.
        if self.precio > 0:
            if self.pago_enlace and self.pago_en_estudio:
                raise ValidationError("Solo podés seleccionar un método de pago: enlace o en estudio.")
            if not self.pago_enlace and not self.pago_en_estudio:
                raise ValidationError("Debés seleccionar al menos un método de pago.")
  
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # Validación para asegurarse de que la imagen sea un archivo de imagen
    def delete(self, *args, **kwargs):
        InscripcionEvento.objects.filter(evento=self).delete()
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d/%m/%Y')}"
    

class InscripcionEvento(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)