from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.http import Http404

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

def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Registrado")
        else:
            data["form"] = formulario

    return render(request, 'app/producto/agregar.html', data)

def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'app/producto/listar.html', data)

def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="app_tienda:listar_productos")
        data["form"] = formulario

    return render(request, 'app/producto/modificar.html', data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="app_tienda:listar_productos")