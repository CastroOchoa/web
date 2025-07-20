from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'celular', 'correo', 'direccion']
from django import forms
import re

class ClientePedidoForm(forms.Form):
    nombre_completo = forms.CharField(
        label="Nombre Completo",
        max_length=50,
        required=True
    )
    celular = forms.CharField(label="Número de Celular", max_length=20, required=True)
    correo = forms.EmailField(label="Correo Electrónico", required=True)
    direccion = forms.CharField(label="Dirección", widget=forms.Textarea, required=True)

    def clean_nombre_completo(self):
        nombre = self.cleaned_data['nombre_completo'].strip()

        # Validar que no esté vacío después de quitar espacios
        if not nombre:
            raise forms.ValidationError("Este campo no puede estar vacío.")

        # Validar que contenga solo letras y espacios
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("Solo se permiten letras y espacios. No se permiten números ni caracteres especiales.")

        return nombre