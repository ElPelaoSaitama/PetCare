from django.urls import path
from . import views

app_name = 'app_clinica'
urlpatterns = [
    path('', views.home, name="home" ),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('registro/', views.register, name="registro"),
    path('contact/', views.contact, name="contact"),
    path('user/', views.user, name="user"),
    path('editar-perfil/', views.editarPerfil, name='editar_perfil'),
    path('editar-password/', views.editarPassword, name="editar_password"),
    path('historial-medico/', views.historialMedico, name="historial_medico"),
    path('tus-mascotas/', views.mascotaCliente, name="mascota_cliente"),
    path('editar-mascota/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),

]
