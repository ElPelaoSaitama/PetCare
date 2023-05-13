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
    

]
