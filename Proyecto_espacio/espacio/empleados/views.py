from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Empleado
from .forms import EmpleadoForm
from django.views.decorators.http import require_POST

@login_required
def lista_empleados(request):
    # Muestra empleados activos e inactivos por separado
    activos = Empleado.objects.filter(activo=True)
    papelera = Empleado.objects.filter(activo=False)
    return render(request, 'empleados/lista_empleados.html', {
        'empleados': activos,
        'papelera': papelera,
    })

@login_required
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'empleados/detalle_empleado.html', {'empleado': empleado})

@login_required
def crear_empleado(request):
    # Maneja la creación de nuevos empleados
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()

    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista_empleados.html', {
        'empleados': empleados,
        'form': form,
        'mostrar_modal': True
    })

@login_required
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)

    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista_empleados.html', {
        'empleados': empleados,
        'form': form,
        'mostrar_modal': True
    })

@require_POST
@login_required
def desactivar_empleado(request, pk):
    # Desactiva un empleado (lo mueve a la papelera)
    empleado = get_object_or_404(Empleado, pk=pk)
    fecha_baja = request.POST.get('fecha_baja')

    if fecha_baja:
        empleado.fecha_baja = fecha_baja
        empleado.activo = False
        empleado.save()
    return redirect('lista_empleados')

@require_POST
@login_required
def reactivar_empleado(request, pk):
    # Reactiva un empleado (lo saca de la papelera)
    empleado = get_object_or_404(Empleado, pk=pk)
    fecha_alta = request.POST.get('fecha_alta')

    if fecha_alta:
        empleado.fecha_alta = fecha_alta
        empleado.fecha_baja = None
        empleado.activo = True
        empleado.save()
    return redirect('lista_empleados')

@require_POST
@login_required
def eliminar_empleado(request, pk):
    # Elimina permanentemente un empleado
    empleado = get_object_or_404(Empleado, pk=pk)
    empleado.delete()
    return redirect('lista_empleados')