from django.db import models
import os

class Empleado(models.Model):
    # Campos básicos del empleado
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    instagram = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    # Campos de estado y fechas
    fecha_alta = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    # Campos para la web pública
    imagen_perfil = models.ImageField(upload_to='empleados/', blank=True, null=True)
    mostrar_en_web = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)  #Campor para saber si el empleado esta activo!
    
    # Método para eliminar la imagen al borrar el empleado
    def delete(self, *args, **kwargs):
        if self.imagen_perfil and os.path.isfile(self.imagen_perfil.path):
            os.remove(self.imagen_perfil.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"