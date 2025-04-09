from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Empleado
from .forms import EmpleadoForm

@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista_empleados.html', {'empleados': empleados})

@login_required
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'empleados/detalle_empleado.html', {'empleado': empleado})

@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/empleado_form.html', {'form': form})

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
    return render(request, 'empleados/empleado_form.html', {'form': form})

@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('lista_empleados')
    return render(request, 'empleados/confirmar_eliminar.html', {'empleado': empleado})
