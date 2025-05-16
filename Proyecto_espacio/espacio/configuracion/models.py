from django.db import models
from multiselectfield import MultiSelectField

class Configuracion(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    nombre_estudio = models.CharField(max_length=100, default='Estudio')
    telefono = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    cuit = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    maps = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    texto_hero = models.TextField(blank=True)
    mensaje_whatsapp_plan = models.CharField(max_length=255, blank=True)
    mensaje_whatsapp_evento = models.CharField(max_length=255, blank=True)

    dias_habilitados = MultiSelectField(choices=DIAS_SEMANA, blank=True)
    horario_semana_inicio = models.TimeField(blank=True, null=True)
    horario_semana_fin = models.TimeField(blank=True, null=True)
    horario_sabado_inicio = models.TimeField(blank=True, null=True)
    horario_sabado_fin = models.TimeField(blank=True, null=True)
    horario_domingo_inicio = models.TimeField(blank=True, null=True)
    horario_domingo_fin = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "Configuración del sitio"

