# Usa una imagen base oficial de Python
FROM python:3.10-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Establece variables de entorno para que Python no escriba .pyc y la salida sea no bufferizada
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia el archivo requirements.txt y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación
# Asegúrate de copiar la carpeta 'espacio' que contiene manage.py y el proyecto principal
# y también tu carpeta 'static'
COPY . /app

# Navega al directorio donde está manage.py
WORKDIR /app/espacio

# Exponer el puerto en el que Gunicorn va a escuchar (Cloud Run inyecta la variable PORT)
ENV PORT 8000
EXPOSE 8000

# Comando para correr la aplicación
# Usaremos Gunicorn, un servidor WSGI para Django
CMD gunicorn espacio.wsgi:application --bind 0.0.0.0:$PORT