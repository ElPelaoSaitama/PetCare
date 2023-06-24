from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'app_clinica'
urlpatterns = [
    path('', views.home, name="home" ),
    path('accounts/login/', views.custom_login, name='custom_login'),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('registro/', views.register, name="registro"),
    path('contact/', views.contact, name="contact"),
    path('get_agendas/', views.get_agendas, name='get_agendas'),
    path('obtener-agendas/', views.obtener_agendas, name='obtener_agendas'),

    #Seccion perfil y edicion 
    path('user/', views.user, name="user"),
    path('editar-perfil/', views.editarPerfil, name='editar_perfil'),
    path('editar-password/', views.editarPassword, name="editar_password"),
    path('historial-medico/', views.historialMedico, name="historial_medico"),
    path('tus-mascotas/', views.mascotaCliente, name="mascota_cliente"),
    path('editar-mascota/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('nueva-mascota/',views.agregarMascota, name="agregar_mascota"),
    path('generar-pdf/<int:mascota_id>/', views.generar_pdf, name='generar_pdf'),
    path('compras/', views.compras_cliente, name='compras_cliente'),
    path('obtener_razas/', views.get_razas, name='obtener_razas'),
    
    
    path('eliminar-agendamiento/<int:consulta_id>/', views.eliminarAgendamiento, name='eliminar_agendamiento'),
    path('editar-agendamiento/<int:consulta_id>/', views.editarAgendamiento, name='editar_agendamiento'),

    #Seccion colaboradores
    path('colaborador-login/', views.colaborador_login, name='colaborador_login'),
    path('colaborador/', views.colaborador, name="colaborador"),
    path('citas-colaborador/', views.citasColaborador, name="citas_colaborador"),
    path('diagnostico/<int:consulta_id>/', views.diagnostico, name="diagnostico"),
    path('recordatorio/', views.recordatorio, name='recordatorio'),
    path('enviar-correo/<int:agendamiento_id>/', views.enviar_correo, name='enviar_correo'),
    path('editar-agendamiento-colaborador/<int:agendamiento_id>/', views.editar_agendamiento, name='editar_agendamiento_colaborador'),
    path('buscar-clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),


]
