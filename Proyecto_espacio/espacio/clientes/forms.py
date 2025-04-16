from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'dni', 'telefono', 'mail', 'plan', 'dias', 'hora', 'estado']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'dias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Martes y Jueves'}),
            'hora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10:00hs'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }