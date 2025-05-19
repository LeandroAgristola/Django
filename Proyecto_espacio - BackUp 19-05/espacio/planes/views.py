from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan
from .forms import PlanForm
from django.http import JsonResponse


@login_required
def listado_planes(request):
    planes_activos = Plan.objects.filter(activo=True)
    planes_inactivos = Plan.objects.filter(activo=False)
    return render(request, 'planes/lista_planes.html', {
        'planes_activos': planes_activos,
        'planes_inactivos': planes_inactivos
    })

@login_required
def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planes:lista_planes')
    else:
        form = PlanForm()
    return render(request, 'planes/form_plan.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan_modificado = form.save(commit=False)
            plan_modificado.activo = True
            plan_modificado.save()
            return redirect('planes:lista_planes')  # ← nombre unificado
    else:
        form = PlanForm(instance=plan)
    return render(request, 'planes/form_plan.html', {'form': form, 'plan': plan})  # ← nombre corregido


@login_required
def desactivar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.activo = False
    plan.save()
    return redirect('planes:lista_planes')

@login_required
def reactivar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.activo = True
    plan.save()
    return redirect('planes:lista_planes')

@login_required
def eliminar_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('planes:lista_planes')
    return render(request, 'planes/confirmar_eliminar.html', {'plan': plan})

@login_required
def estadisticas_planes(request):
    planes = Plan.objects.filter(activo=True)
    datos = []
    
    for plan in planes:
        count = plan.cliente_set.filter(activo=True).count()
        if count > 0:  # Solo mostramos planes con clientes
            datos.append({
                'plan': plan.nombre,
                'clientes': count
            })
    
    return JsonResponse({
        'labels': [d['plan'] for d in datos],
        'data': [d['clientes'] for d in datos],
        'total': sum([d['clientes'] for d in datos])
    })