from django.db import models
import os

class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    instagram = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    ingreso = models.DateField()
    imagen_perfil = models.ImageField(upload_to='empleados/', blank=True, null=True)
    mostrar_en_web = models.BooleanField(default=False)
    
    def delete(self, *args, **kwargs):
        if self.imagen_perfil and os.path.isfile(self.imagen_perfil.path):
            os.remove(self.imagen_perfil.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"