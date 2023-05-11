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
    

]
