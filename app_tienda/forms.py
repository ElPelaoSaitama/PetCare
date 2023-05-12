from django import forms
from .models import Producto, Marca, Categoria, SubCategoria


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    precio = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}))
    stock = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}))
    descripcion = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    subCategoria = forms.ModelChoiceField(queryset=SubCategoria.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Producto
        fields = '__all__'
