from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'email', 'direccion', 'telefono', 'instagram', 'ingreso', 'imagen_perfil', 'mostrar_en_web']

    def clean_mostrar_en_web(self):
        mostrar_en_web = self.cleaned_data.get('mostrar_en_web')
        if mostrar_en_web:
            if Empleado.objects.filter(mostrar_en_web=True).count() >= 4:
                raise forms.ValidationError("Solo se pueden mostrar 4 empleados en la web pública.")
        return mostrar_en_web