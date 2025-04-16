from django.db import models

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    detalle = models.TextField()
    cantidad_dias = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mostrar_en_web = models.BooleanField(default=True)
    
    @property
    def precio_formateado(self):
        return f"{self.precio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def __str__(self):
        return self.nombre
    