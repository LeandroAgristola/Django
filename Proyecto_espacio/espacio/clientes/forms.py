from django import forms
from .models import Cliente, Plan

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'dni', 'telefono', 'mail', 'plan', 'estado', 'fecha_alta', 'fecha_baja']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'fecha_alta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'plan' in self.fields:
            # Configurar las opciones normalmente
            self.fields['plan'].queryset = Plan.objects.all()