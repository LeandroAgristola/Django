from django.db import models

class Configuracion(models.Model):
    nombre_estudio = models.CharField(max_length=100, default='Estudio')
    cuit = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    maps = models.URLField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    horario_semana = models.CharField(max_length=255, blank=True)
    horario_sabado = models.CharField(max_length=255, blank=True)
    texto_hero = models.TextField(blank=True)

    def __str__(self):
        return "Configuración del sitio"

# Create your models here.
