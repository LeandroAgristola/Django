from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    """
    Vista para manejar el inicio de sesión de usuarios.
    - Si el método es POST, autentica al usuario con las credenciales proporcionadas.
    - Si la autenticación es exitosa, redirige al panel de administración.
    - Si falla, muestra un mensaje de error en la plantilla de login.
    """
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
    """
    Vista del panel de administración principal.
    - Requiere que el usuario esté autenticado.
    - Muestra el template del panel con estadísticas y gráficos.
    """
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def panel(request):
    """
    Vista del panel de administración principal.
    - Requiere que el usuario esté autenticado.
    - Muestra el template del panel con estadísticas y gráficos.
    """
    return render(request, 'management/panel.html')

