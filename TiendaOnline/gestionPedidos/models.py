from django.db import models

# Create your models here.

class Clientes(models.Model): #creamos la primera tabla
    nombre=models.CharField(max_length=30) #creamos un nueva clase de tipo texto con 30 caracteres como maximo
    direccion=models.CharField(max_length=50)
    email=models.EmailField(blank=True, null=True) #establecemos el campo como "opcional"
    telefono=models.CharField(max_length=12)

    def __str__(self): 
        return self.nombre #Retornamos el nombre del campo en el panel de admin

class Articulos(models.Model): #creamos la segunda tabla
    nombre=models.CharField(max_length=30)
    seccion=models.CharField(max_length=30)
    precio=models.IntegerField()

    def __str__(self): 
        return self.nombre #Retornamos el nombre del campo en el panel de admin

class Pedidos(models.Model): #creamos la tercera tabla
    numero=models.IntegerField()
    fecha=models.DateField()
    entregado=models.BooleanField()

    



