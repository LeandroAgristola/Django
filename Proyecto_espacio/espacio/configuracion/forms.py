from django import forms
from .models import Configuracion

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'
        widgets = {
            'nombre_estudio': forms.TextInput(attrs={
                'placeholder': 'Nombre del estudio',
                'class': 'form-control'
            }),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Dirección',
                'class': 'form-control'
            }),
            'horario_semana': forms.TextInput(attrs={
                'placeholder': 'Lunes a Viernes de 8 a 21 hs.',
                'class': 'form-control'
            }),
            'horario_sabado': forms.TextInput(attrs={
                'placeholder': 'Sábados de 9 a 13 hs.',
                'class': 'form-control'
            }),
            'maps': forms.TextInput(attrs={
                'placeholder': 'https://maps.google.com/...',
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Teléfono',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'estudio@mail.com',
                'class': 'form-control'
            }),
            'instagram': forms.TextInput(attrs={
                'placeholder': 'https://instagram.com/...',
                'class': 'form-control'
            }),
            'facebook': forms.TextInput(attrs={
                'placeholder': 'https://facebook.com/...',
                'class': 'form-control'
            }),
            'youtube': forms.TextInput(attrs={
                'placeholder': 'https://youtube.com/...',
                'class': 'form-control'
            }),
            'whatsapp': forms.TextInput(attrs={
                'placeholder': 'Teléfono de WhatsApp',
                'class': 'form-control'
            }),
            'texto_hero': forms.Textarea(attrs={
                'placeholder': 'Texto para la sección de héroe',
                'class': 'form-control',
                'rows': 3
            }),
            'cuit': forms.TextInput(attrs={
                'placeholder': 'CUIT',
                'class': 'form-control'
            }),

            
        }
