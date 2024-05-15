from django import forms 
from .models import Productos

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'categoria', 'stock', 'precio', 'imagen']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción del producto...'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la categoría del producto...'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad en stock...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio del producto...'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }