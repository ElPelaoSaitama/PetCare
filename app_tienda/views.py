from django.shortcuts import render
from .models import Producto

#Pagina de categorias de la tienda
def categorias(request):
    return render(request, 'app/categorias.html')

def catPerros(request):
    productos = Producto.objects.filter(categoria_id=1)
    data  = {
        'productos': productos,
    }
    return render(request, 'app/catPerros.html', data)

def catGatos(request):
    productos = Producto.objects.filter(categoria_id=2)
    data  = {
        'productos': productos,
    }
    return render(request, 'app/catGatos.html', data)

def catExoticos(request):
    productos = Producto.objects.filter(categoria_id=3)
    data  = {
        'productos': productos,
    }
    return render(request, 'app/catExoticos.html', data)

def catFarmacia(request):
    productos = Producto.objects.filter(categoria_id=4)
    data  = {
        'productos': productos,
    }
    return render(request, 'app/catFarmacia.html', data)