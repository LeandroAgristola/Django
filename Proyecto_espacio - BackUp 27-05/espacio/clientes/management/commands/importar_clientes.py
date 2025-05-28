import json
from django.core.management.base import BaseCommand
from clientes.models import Cliente
from planes.models import Plan
from calendario.models import Turno
from datetime import datetime, timedelta
from django.db.models import Q

class Command(BaseCommand):
    help = 'Importa clientes desde un archivo JSON y genera turnos'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta del archivo JSON con los clientes')

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)

        dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        for entry in data:
            try:
                plan = Plan.objects.get(nombre=entry['plan'])
                fecha_alta = datetime.strptime(entry['fecha_alta'], "%Y-%m-%d").date()

                cliente, creado = Cliente.objects.get_or_create(
                    mail=entry['mail'],
                    defaults={
                        'nombre': entry['nombre'],
                        'apellido': entry['apellido'],
                        'dni': entry['dni'],
                        'telefono': entry.get('telefono', ''),
                        'plan': plan,
                        'dias': entry.get('dias'),
                        'hora': entry.get('hora'),
                        'tipo': entry.get('tipo', 'regular'),
                        'estado': entry.get('estado', 'pendiente'),
                        'fecha_alta': fecha_alta,
                        'ultima_confirmacion': datetime.strptime(entry['ultima_confirmacion'], "%Y-%m-%d").date() if entry.get('ultima_confirmacion') else None,
                        'activo': entry.get('activo', True)
                    }
                )

                if creado:
                    self.stdout.write(self.style.SUCCESS(f"✔ Cliente {cliente} creado"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠ Cliente ya existía: {cliente.mail}"))
                
                # Generar turnos
                self.generar_turnos(cliente)

            except Plan.DoesNotExist:
                self.stderr.write(f"❌ Plan no encontrado: {entry['plan']}")
            except Exception as e:
                self.stderr.write(f"❌ Error con cliente {entry.get('nombre')}: {str(e)}")

    def generar_turnos(self, cliente):
        dias_seleccionados = [d.strip().lower() for d in cliente.dias.split(',')]
        horas_seleccionadas = [h.strip() for h in cliente.hora.split(',')]

        if len(dias_seleccionados) != len(horas_seleccionadas):
            self.stderr.write(f"❌ Días y horarios desiguales para {cliente}")
            return

        dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        fecha_inicio = cliente.fecha_alta
        fecha_limite = fecha_inicio + timedelta(days=180)

        cliente.turnos.filter(fecha__gte=fecha_inicio).delete()

        for dia, hora in zip(dias_seleccionados, horas_seleccionadas):
            try:
                dia_idx = dias_esp.index(dia)
                hora_obj = datetime.strptime(hora, "%H:%M").time()

                fecha = fecha_inicio
                delta = (dia_idx - fecha.weekday() + 7) % 7
                fecha += timedelta(days=delta)

                while fecha <= fecha_limite:
                    ocupados = Turno.objects.filter(
                        fecha=fecha,
                        hora=hora_obj
                    ).filter(
                        Q(cliente__fecha_alta__lte=fecha) &
                        (Q(cliente__fecha_baja__isnull=True) | Q(cliente__fecha_baja__gte=fecha))
                    ).count()

                    if ocupados < 6:
                        Turno.objects.get_or_create(
                            cliente=cliente,
                            fecha=fecha,
                            hora=hora_obj
                        )

                    fecha += timedelta(days=7)

            except Exception as e:
                self.stderr.write(f"❌ Error generando turno {dia} {hora} para {cliente}: {str(e)}")

            
#python manage.py importar_clientes ../extras/clientes.json