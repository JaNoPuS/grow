"""
    INVENTARIO FORMS
"""

from django import forms
from .models import Categoria, Producto, MovimientosInventario

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion','precio','categoria','cantidad_disponible','cantidad_minima','imagen','estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del producto'}),
            'estado': forms.Select(choices=Producto.estado.field.choices),
        }

        def clean_precio(self):
            precio = self.cleaned_data.get('precio')
            if precio < 0:
                raise forms.ValidationError("El precio debe ser superior a 0 pesos!")
            return precio

class MovimientosInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientosInventario
        fields = ['producto', 'tipo_movimiento', 'cantidad_movimiento']
        widgets = {
            'tipo_movimiento': forms.Select(choices=MovimientosInventario.tipo_movimiento.field.choices),
        }