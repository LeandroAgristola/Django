from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            return render(request, 'management/login.html', {
                'message': 'Credenciales inválidas. Intente nuevamente.'
            })
    return render(request, 'management/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def panel(request):
    return render(request, 'management/panel.html')

