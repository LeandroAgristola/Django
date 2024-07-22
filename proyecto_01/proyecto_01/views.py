from django.http import HttpResponse #importamos el modulo de respuesta HTTP de django
import datetime #importamos el modulo de fecha y hora
from django.template import Template, Context #importamos los modulos template y context de django
from django.template.loader import get_template #importamos el metodo cargador con "get_template" para facilitar la carga de documento 
from django.shortcuts import render
import os #se utiliza para construir de manera segura la ruta de la planilla

### Creamos el objeto ###

class Persona(object):
    
    def __init__(self, nombre, apellido):

        self.nombre=nombre

        self.apellido=apellido

### Aplicando Plantillas ####

def saludo(request): 

    p1=Persona("Carlos", "Fernandez") #inicializamos el objeto
    ahora=datetime.datetime.now() #asignamos a la variable ahora la hora actual
    temasTotal=["Tema 1","Tema 2","Tema 3"]
    contexto = {"nombre_persona":p1.nombre, "apellido_persona":p1.apellido, "momento_actual":ahora, "temas":temasTotal}

    #mediante el modulo shortcuts directamente en el return generamos todos los pasos

    return render(request,"index.html",contexto)

def contenido(request):

    ahora=datetime.datetime.now() #asignamos a la variable ahora la hora actual
    contexto={"momento_actual":ahora}

    return render(request, "contenido.html", contexto)






    #try:
    #    ruta_plantilla = os.path.join("C:/Users/Leandro/Documents/Drive/Curso/Python/Proyectos_Django/proyecto_01/plantillas/index.html")
    #    with open(ruta_plantilla, 'r') as archivo: #'r' se refiere a "solo lectura"
    #        plantilla = Template(archivo.read())
    #except FileNotFoundError:
    #    return HttpResponse("Error: No se encontró el archivo de la plantilla.", status=404)



v
    ##Creación objeto Template forma no optima##
  
    # 1) Creación objeto Template 

    #doc_externo = get_template('index.html') #utilizamos el metodo loader para cargar la plantilla de nuestra carpeta por defecto declara en setting

    # 2) Creación del contexto
    # Creamos el contexto y le asignamos el diccionario referenciando al objeto
    #contexto = {"nombre_persona":p1.nombre, "apellido_persona":p1.apellido, "momento_actual":ahora, "temas":temasTotal}

    # 3) Renderizado del objeto template
    #documento = doc_externo.render(contexto)

    #return HttpResponse(documento)