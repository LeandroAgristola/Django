from django.core.management.base import BaseCommand
from django.utils import timezone
from clientes.models import Cliente
from datetime import date

class Command(BaseCommand):
    help = 'Resetea los estados de los clientes a pendiente el primer día de cada mes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar ejecución aunque no sea el primer día del mes'
        )

    def handle(self, *args, **options):
        hoy = date.today()
        
        if hoy.day == 1 or options['force']:  # Modificado para aceptar --force
            clientes = Cliente.objects.filter(
                activo=True,
                tipo='regular',
                estado='confirmado'
            ).exclude(
                ultima_confirmacion__month=hoy.month,
                ultima_confirmacion__year=hoy.year
            )
            
            actualizados = clientes.update(estado='pendiente')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✔ Reseteados {actualizados} clientes a estado pendiente'
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE('ℹ Hoy no es el primer día del mes. No se realizaron cambios.')
            )