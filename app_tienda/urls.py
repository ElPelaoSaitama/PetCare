from django.urls import path
from . import views

app_name = 'app_tienda'
urlpatterns = [
    path('', views.categorias, name="categorias"),
    path('catalogoPerros/', views.catPerros, name="catalogoPerros" ),
    path('catalogoGatos/', views.catGatos, name="catalogoGatos" ),
    path('catalogoExoticos/', views.catExoticos, name="catalogoExoticos" ),
    path('catalogoFarmacia/', views.catFarmacia, name="catalogoFarmacia" ),
    path('agregar-producto/', views.agregar_producto, name="agregar_producto" ),
    path('listar-producto/', views.listar_productos, name="listar_productos" ),
    path('modificar-producto/<id>/', views.modificar_producto, name="modificar_producto" ),
    path('eliminar-producto/<id>/', views.eliminar_producto, name="eliminar_producto"),
    path('tienda/', views.tienda, name="tienda"),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),

    path('paypal/', views.simple_checkout, name='simple_checkout'),
    path('success/', views.success, name='success'),
    path('complete/', views.paymentComplete, name='complete'),

    path('compra-exitosa/', views.almacenar_compra_exitosa, name='compra_exitosa'),
    path('generar_boleta/<int:orden_id>/', views.generar_boleta, name='generar_boleta'),
    path('enviar-boleta-por-correo/<int:orden_id>/', views.enviar_boleta_por_correo, name='enviar_boleta_por_correo'),

]
