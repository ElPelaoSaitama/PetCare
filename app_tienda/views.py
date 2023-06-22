from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Producto, Orden, Orden_detail, Categoria, Orden, Orden_detail
from app_clinica.models import Cliente
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
import json, random, requests
from django.contrib.auth.models import User
from django.http import JsonResponse

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

@login_required
def ver_carrito(request):
    # Obtener el carrito de compras desde la sesión del usuario
    request.session["paypal"] = True
    carrito = request.session.get('carrito', {})
    #print(carrito)
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

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el carrito de compras desde la sesión del usuario
    carrito = request.session.get('carrito', {})

    # Verificar si el producto ya está en el carrito
    if str(producto_id) in carrito:
        # Incrementar la cantidad del producto en el carrito
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        # Convertir el producto a un diccionario
        producto_dict = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'imagen': producto.imagen.url if producto.imagen else None
        }

        # Agregar el producto al carrito con cantidad 1
        carrito[str(producto_id)] = {
            'producto': producto_dict,
            'cantidad': 1
        }

    # Actualizar el carrito en la sesión del usuario
    request.session['carrito'] = carrito

    # Mostrar mensaje de éxito
    messages.success(request, f"{producto.nombre} se ha agregado al carrito.")

    # Redireccionar al usuario a la página de productos o al carrito de compras
    return redirect('app_tienda:ver_carrito')


def simple_checkout(request):
    return render(request, 'app/cart/simple_checkout.html')

def paymentComplete(request):
    body = json.loads(request.body)
    sess = request.session.get("data",{"items":[]})
    productos_carro = sess["items"]
    #todos los datos de cabecera
    Oc = Orden()
    Oc.customer=body['customer']
    Oc.ordernum=random.randint(10000,99999)
    Oc.save()
    for item in productos_carro:
        prod=Producto.objects.get(id.item)
        Od=Orden_detail()
        Od.producto=prod
        Od.cant=1
        Od.orden=Oc
        Od.save()
    del request.session['carrito']
    return request('app_tienda:success')

def success(request):
    context = {
        "mensaje": "La compra ha sido exitosa"  # Agrega un mensaje de éxito al contexto
    }
    return render(request, 'app/cart/success.html', context)

def vaciar_carrito(request):
    # Eliminar el contenido de la sesión del carrito
    request.session.pop('carrito', None)
    # Redireccionar a la página de carrito vacío o a donde corresponda
    return redirect('app_tienda:ver_carrito')


import random
import string

def generar_numero_orden():
    # Generar un número de orden único, por ejemplo, combinando letras y números al azar
    caracteres = string.ascii_letters + string.digits
    numero_orden = ''.join(random.choices(caracteres, k=9))
    return numero_orden

def obtener_informacion_cliente(user):
    # Obtener el objeto de cliente asociado al usuario
    cliente = Cliente.objects.get(user=user)

    # Obtener los detalles del cliente
    nombre = user.first_name
    apellido = user.last_name
    fecha_nacimiento = cliente.fecha_nac
    genero = cliente.genero
    numero_telefono = cliente.cellNumber
    direccion = cliente.direccion
    rut = cliente.rut

    # Realizar las operaciones necesarias con los detalles del cliente

    return nombre, apellido, fecha_nacimiento, genero, numero_telefono, direccion, rut

import json
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Orden, Orden_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def get_user_info(user):
    """
    Obtiene la información del usuario.
    """
    nombre = user.first_name
    apellido = user.last_name
    return nombre, apellido

from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist


@login_required
def almacenar_compra_exitosa(request):
    if request.method == 'POST':
        user = request.user

        # Verificar si el usuario tiene un nombre
        if user.first_name:
            nombre = user.first_name.capitalize()
            apellido = user.last_name.capitalize()
        else:
            nombre = ""

        # Crear una nueva instancia de Orden
        orden = Orden()
        orden.ordernum = generar_numero_orden()
        orden.customer = f'{nombre} {apellido}'
        orden.status = True
        orden.save()

        # Obtener los productos del carrito
        data = json.loads(request.body)
        productos_carrito = data.get('carrito')
        imprimir_carrito(request)

        carrito = request.session.get('carrito', {})
        for item in carrito.values():
            producto_dict = item['producto']
            cantidad = item['cantidad']

            producto_nombre = producto_dict['nombre']
            producto_precio = producto_dict['precio']

            try:
                producto = Producto.objects.get(nombre=producto_nombre)
            except ObjectDoesNotExist:
                # Manejar el caso en que el producto no existe en la base de datos
                continue

            orden_detail = Orden_detail()
            orden_detail.producto = producto
            orden_detail.cant = cantidad
            orden_detail.orden = orden
            orden_detail.save()
            print(orden_detail)

        return JsonResponse({'success': True, 'message': 'Compra exitosa'})

    return redirect('app_tienda:ver_carrito')





    

def imprimir_carrito(request):
    carrito = request.session.get('carrito', {})
    for item in carrito.values():
        producto_dict = item['producto']
        cantidad = item['cantidad']

        producto_id = producto_dict['id']
        producto_nombre = producto_dict['nombre']
        producto_precio = producto_dict['precio']

        print(f"id: {producto_id}")
        print(f"Producto: {producto_nombre}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio: {producto_precio}")
        print("---")

    total = sum(item['producto']['precio'] * item['cantidad'] for item in carrito.values())
    print(f"Total: {total}")











