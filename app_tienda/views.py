from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required , permission_required

#Pagina de categorias de la tienda
def categorias(request):
    return render(request, 'app/categorias.html')

def catPerros(request):
    productos = Producto.objects.filter(categoria__nombre='Perros')
    data = {
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

@permission_required('app_tienda.add_producto')
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

@permission_required('app_tienda.view_producto')
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

@permission_required('app_tienda.change_producto')
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

@permission_required('app_tienda.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="app_tienda:listar_productos")

def tienda(request):
    return render (request, 'app/producto/tienda.html')

from django.shortcuts import render

def ver_carrito(request):
    # Obtener el carrito de compras desde la sesión del usuario
    carrito = request.session.get('carrito', {})
    productos_carrito = []
    total = 0

    # Recorrer los productos en el carrito
    for item in carrito.values():
        producto_dict = item['producto']
        cantidad = item['cantidad']

        # Crear un objeto Producto a partir del diccionario
        producto = Producto(
            id=producto_dict['id'],
            nombre=producto_dict['nombre'],
            precio=producto_dict['precio'],
            imagen=producto_dict['imagen']
        )

        subtotal = producto.precio * cantidad
        total += subtotal

        # Crear un objeto auxiliar para almacenar el producto y la cantidad
        producto_carrito = {
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        }

        productos_carrito.append(producto_carrito)

    data = {
        'productos_carrito': productos_carrito,
        'total': total
    }

    return render(request, 'app/cart/carrito_compras.html', data)


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Producto

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el carrito de compras desde la sesión del usuario
    carrito = request.session.get('carrito', {})

    # Verificar si el producto ya está en el carrito
    if producto_id in carrito:
        # Incrementar la cantidad del producto en el carrito
        carrito[producto_id]['cantidad'] += 1
    else:
        # Convertir el producto a un diccionario
        producto_dict = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'imagen': producto.imagen.url if producto.imagen else None
        }

        # Agregar el producto al carrito con cantidad 1
        carrito[producto_id] = {
            'producto': producto_dict,
            'cantidad': 1
        }

    # Actualizar el carrito en la sesión del usuario
    request.session['carrito'] = carrito

    # Mostrar mensaje de éxito
    messages.success(request, f"{producto.nombre} se ha agregado al carrito.")

    # Redireccionar al usuario a la página de productos o al carrito de compras
    return redirect('app_tienda:ver_carrito')



from django.http import JsonResponse

def vaciar_carrito(request):
    # Eliminar el contenido de la sesión del carrito
    request.session.pop('carrito', None)
    # Redireccionar a la página de carrito vacío o a donde corresponda
    return redirect('app_tienda:ver_carrito')



