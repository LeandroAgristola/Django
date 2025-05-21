from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import EventoForm, InscribirClienteForm
from .models import InscripcionEvento, Evento
from clientes.models import Cliente
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import date
#importaciones para exportar pdf
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.templatetags.static import static
import os
from reportlab.pdfgen import canvas # exportar_pdf

@login_required
def lista_eventos(request):
    eventos = Evento.objects.filter(estado=True)
    papelera = Evento.objects.filter(estado=False)
    form = EventoForm()
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'hoy': date.today(),
        'papelera': papelera,
        'form': form,
    })

@login_required
def detalle_eventos(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_eventos.html', {'evento': evento})

@login_required
def detalle_eventos(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle_eventos.html', {'evento': evento})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento creado correctamente.")
            return redirect('eventos_admin:lista_eventos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = EventoForm()

    return render(request, 'eventos/evento_form.html', {'form': form})


@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente.")
            return redirect('eventos_admin:lista_eventos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/evento_form.html', {
        'form': form,
        'evento': evento
    })

@require_POST
@login_required
def desactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    cantidad_inscriptos = InscripcionEvento.objects.filter(evento=evento).count()

    InscripcionEvento.objects.filter(evento=evento).delete()

    evento.cupos += cantidad_inscriptos
    evento.estado = False
    evento.save()

    messages.success(request, f"Evento desactivado. Se restauraron {cantidad_inscriptos} cupos.")
    return redirect('eventos_admin:lista_eventos')

@require_POST
@login_required
def reactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    new_fecha_str = request.POST.get('fecha_alta')
    new_hora_str = request.POST.get('hora_alta')

    try:
        new_fecha = datetime.strptime(new_fecha_str, '%Y-%m-%d').date()
        new_hora = datetime.strptime(new_hora_str, '%H:%M').time()
    except ValueError:
        messages.error(request, "Formato de fecha u hora incorrecto.")
        return redirect('eventos_admin:lista_eventos')

    nueva_fecha_hora = datetime.combine(new_fecha, new_hora)
    actual_fecha_hora = datetime.combine(evento.fecha, evento.hora)
    ahora = datetime.now().replace(second=0, microsecond=0)

    if nueva_fecha_hora == actual_fecha_hora:
        messages.error(request, "La nueva fecha y hora deben ser distintas a la actual.")
        return redirect('eventos_admin:lista_eventos')

    if nueva_fecha_hora < ahora:
        messages.error(request, "La nueva fecha y hora no pueden ser anteriores al momento actual.")
        return redirect('eventos_admin:lista_eventos')

    evento.fecha = new_fecha
    evento.hora = new_hora
    evento.estado = True
    evento.save()
    return redirect('eventos_admin:lista_eventos')

@require_POST
@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.delete()
    return redirect('eventos_admin:lista_eventos')

@login_required
def inscribir_cliente(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        form = InscribirClienteForm(request.POST)
        if form.is_valid():
            tipo_cliente = form.cleaned_data['tipo_cliente']
            estado = form.cleaned_data['estado']

            if tipo_cliente == 'cargado':
                email = request.POST.get('cliente_id')
                cliente = Cliente.objects.get(mail=email)

            else: 
                email = form.cleaned_data['email']
                if Cliente.objects.filter(mail=email).exists():
                    messages.error(request, "El correo electrónico ya está registrado.")
                    return redirect('eventos_admin:inscribir_cliente', evento_id=evento.id)

                cliente = Cliente.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    apellido=form.cleaned_data['apellido'],
                    dni=int(datetime.now().timestamp()), 
                    mail=email,
                    telefono=form.cleaned_data['telefono'],  
                    plan=None,
                    tipo='eventual',
                    estado=estado,
                    activo=True,
                )
            if InscripcionEvento.objects.filter(evento=evento, cliente=cliente).exists():
                messages.warning(request, "Este cliente ya está inscripto en el evento.")
                return redirect('eventos_admin:inscribir_cliente', evento_id=evento.id)

            evento.cupos = max(0, evento.cupos - 1) 
            evento.save()

            inscripcion = InscripcionEvento.objects.create(
                evento=evento,
                nombre=cliente.nombre,
                apellido=cliente.apellido,
                email=cliente.mail,
                telefono=cliente.telefono,
                estado=estado,
                cliente=cliente
            )

            messages.success(request, "Cliente inscrito correctamente.")
            return redirect('eventos_admin:detalle_eventos', pk=evento.id)
        
        else:
            messages.error(request, "Error al inscribir cliente.")
    else:
        form = InscribirClienteForm()

    return render(request, 'eventos/inscribir_cliente.html', {
        'form': form,
        'evento': evento,
        'clientes': clientes
    })

@require_POST
@login_required
def confirmar_pago_evento(request, inscripcion_id):
    inscripcion = get_object_or_404(InscripcionEvento, id=inscripcion_id)
    inscripcion.estado = 'confirmado'
    inscripcion.save()
    messages.success(request, "Pago confirmado.")
    return redirect('eventos_admin:detalle_eventos', pk=inscripcion.evento.id)

@require_POST
@login_required
def eliminar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(InscripcionEvento, id=inscripcion_id)
    evento = inscripcion.evento

    evento.cupos += 1
    evento.save()

    inscripcion.delete()
    messages.success(request, "Inscripción eliminada y cupo liberado.")
    return redirect('eventos_admin:detalle_eventos', pk=evento.id)

@login_required
def exportar_inscriptos_pdf(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = evento.inscripcionevento_set.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="inscriptos_{evento.titulo}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    logo_path = 'C:/Users/Leandro/Documents/ReposGit/Django/Proyecto_espacio/static/logo/logo.png'
    if os.path.exists(logo_path):
        x = 15 * cm
        y = height - 5 * cm 
        c.drawImage(logo_path, x, y, width=4*cm, height=4*cm, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*cm, height - 2*cm, "Listado de Inscriptos")

    c.setFont("Helvetica", 10)
    c.drawString(1*cm, height - 3*cm, f"Evento: {evento.titulo}")
    c.drawString(1*cm, height - 3.6*cm, f"Fecha: {evento.fecha.strftime('%d/%m/%Y')} - Hora: {evento.hora.strftime('%H:%M')} hs")

    data = [["Nombre y Apellido", "Email", "Teléfono", "Estado"]]
    for ins in inscripciones:
        data.append([
            f"{ins.nombre} {ins.apellido}",
            ins.email,
            ins.telefono,
            ins.get_estado_display()
        ])

    table = Table(data, colWidths=[6*cm, 6*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightyellow])
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 1*cm, height - 5.5*cm - len(data)*0.5*cm)

    c.showPage()
    c.save()

    return response

@login_required
def estadisticas_eventos(request):
    rango = request.GET.get('rango', '4')  
    
    hoy = timezone.now().date()
    
    eventos = Evento.objects.filter(
        fecha__lte=hoy
    ).order_by('-fecha', '-hora')
    
    if rango.isdigit():
        eventos = eventos[:int(rango)]
    else:
        eventos = eventos[:4] 

    data = {
        'labels': [],
        'cupos': [],
        'inscriptos': [],
        'porcentajes': [],
        'promedio_ocupacion': 0,
        'cancelados': 0
    }

    total_porcentaje = 0
    for evento in eventos:
        inscriptos = evento.inscripcionevento_set.count()
        porcentaje = (inscriptos / evento.cupos) * 100 if evento.cupos > 0 else 0
        total_porcentaje += porcentaje
        
        data['labels'].append(evento.titulo[:20] + ('...' if len(evento.titulo) > 20 else ''))
        data['cupos'].append(evento.cupos)
        data['inscriptos'].append(inscriptos)
        data['porcentajes'].append(round(porcentaje))
        
        if not evento.estado:
            data['cancelados'] += 1

    if eventos:
        data['promedio_ocupacion'] = round(total_porcentaje / len(eventos))

    return JsonResponse(data)