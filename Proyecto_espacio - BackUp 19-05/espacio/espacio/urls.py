from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webPublic.urls')),
    path('management/empleados/', include('empleados.urls')),
    path('management/', include('management.urls')),
    path('management/eventos/', include('eventos.urls', namespace='eventos_admin')),
    path('management/planes/', include('planes.urls')),
    path('management/clientes/', include('clientes.urls')),
    path('management/configuracion', include('configuracion.urls')),
    path('management/calendario/', include('calendario.urls', namespace='calendario')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)