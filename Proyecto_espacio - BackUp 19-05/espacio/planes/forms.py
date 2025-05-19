from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['nombre', 'detalle', 'cantidad_dias', 'precio', 'mostrar_en_web']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del plan'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del plan', 'rows': 3}),
            'cantidad_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre 1 y 7'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'mostrar_en_web': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_cantidad_dias(self):
        dias = self.cleaned_data['cantidad_dias']
        if dias < 1 or dias > 7:
            raise forms.ValidationError("La cantidad de días debe estar entre 1 y 7.")
        return dias