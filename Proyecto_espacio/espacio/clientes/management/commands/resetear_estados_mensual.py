from django.core.management.base import BaseCommand
from django.utils import timezone
from clientes.models import Cliente
from datetime import date

class Command(BaseCommand):
    help = 'Resetea los estados de los clientes a pendiente el primer día de cada mes'

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        
        if hoy.day == 1:  # Solo ejecutar el primer día del mes
            clientes = Cliente.objects.filter(activo=True)
            actualizados = 0
            
            for cliente in clientes:
                if cliente.estado != 'pendiente':
                    cliente.estado = 'pendiente'
                    cliente.save()
                    actualizados += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✔ Reseteados {actualizados}/{clientes.count()} clientes a estado pendiente'
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE('ℹ Hoy no es el primer día del mes. No se realizaron cambios.')
            )