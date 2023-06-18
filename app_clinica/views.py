from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login
from django.forms import DateInput
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm, ClienteForm, ChangePasswordForm, MascotaForm, AgregarMascotaForm, DiagnosticoForm, EditarAgendamientoForm,EditAgendamientoColaborador,EditarClienteForm
from .models import Categoria, Veterinario, Peluquera, Mascota, Agendamiento, Cliente, Agenda, Diagnostico
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.db.models.functions import Upper

# importe para pdf
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

#importes para email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

#Importes para js del perfil
from django.views.generic import ListView
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
def es_veterinario(user):
    return user.groups.filter(name='Veterinarios').exists()
def es_colaboradores(user):
    return user.groups.filter(name='Colaboradores').exists()


def custom_login(request):
    if request.method == 'POST':
        # Obtén los valores del formulario
        email = request.POST['email']
        password = request.POST['password']

        # Autenticar al usuario
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Credenciales válidas, el usuario existe y la contraseña es correcta
            # Inicia sesión al usuario
            login(request, user)
            # Redirige a la página de inicio o a la página deseada después del inicio de sesión exitoso
            return redirect('app_clinica:home')
        else:
            # Credenciales incorrectas
            # Muestra un mensaje de error utilizando el sistema de mensajes de Django
            error_message = 'Credenciales incorrectas'
            messages.error(request, error_message)

    # Renderiza la página de inicio de sesión con los mensajes
    return render(request, 'registration/login.html')







def home(request):
    data = {
        'form': ContactoForm(),
        'show_link' : not es_veterinario(request.user)
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Mensaje enviado"
        else:
            data["form"] = formulario

    return render(request,'app/home.html',data)

@login_required
def agendamiento(request):
    categoria = Categoria.objects.all()
    veterinario = Veterinario.objects.all()

    data = {
        'categoria': categoria,
        'veterinario': veterinario
    }

    if request.method == 'POST':
        formulario = AgendamientoForm(request.POST, request.FILES, request=request)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha agendado la hora.')
            return redirect('app_clinica:agendamiento')
        else:
            data["form"] = formulario
            print(formulario.errors)  # Imprimir los errores del formulario en la consola para depuración
    else:
        formulario = AgendamientoForm(request=request)
        data["form"] = formulario

    return render(request, 'app/agendamiento.html', data)

def get_agendas(request):
    categoria_id = request.GET.get('categoria_id')
    agendas_disponibles = Agenda.objects.filter(
        categoria_id=categoria_id,
        dia__gte=timezone.now().date(),
        agendamiento__isnull=True
    )
    options = [{'id': agenda.id, 'nombre': str(agenda)} for agenda in agendas_disponibles]
    return JsonResponse(options, safe=False)

def obtener_agendas(request):
    categoria_id = request.GET.get('categoria_id')
    agendas_disponibles = Agenda.objects.filter(
        categoria_id=categoria_id,
        dia__gte=timezone.now().date(),
        agendamiento__isnull=True
    )
    options = [{'id': agenda.id, 'nombre': str(agenda)} for agenda in agendas_disponibles]
    return JsonResponse(options, safe=False)

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="login")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)

def contact(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje']

        template = render_to_string('app/email_template.html', {
            'nombre' : nombre,
            'correo' : correo,
            'mensaje' : mensaje
        })

        email = EmailMessage(
          asunto,
          template,
          settings.EMAIL_HOST_USER,
          ['petcarevetter@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request,'Se ha enviado tu correo.')
        return redirect("app_clinica:home")

@login_required        
def user(request):
    return render(request,"app/user.html")   

@login_required
def historialMedico(request):
    cliente = request.user.cliente
    mascotas = Mascota.objects.filter(dueno=cliente)
    consultas = Agendamiento.objects.filter(mascota__in=mascotas).order_by('-agenda__dia')

    detalles_consulta = []
    fecha_actual = date.today()

    for consulta in consultas:
        mascota_nombre = consulta.mascota.nombre
        agenda = consulta.agenda
        horario_inicio, horario_fin = agenda.get_horario_display().split(" a ")
        horario = f"{horario_inicio} a {horario_fin}"

        if agenda.dia < fecha_actual:
            detalles_consulta.append((consulta, mascota_nombre, horario, True))
        else:
            detalles_consulta.append((consulta, mascota_nombre, horario, False))

    context = {
        'detalles_consulta': detalles_consulta
    }
    return render(request, 'app/historial_clinico.html', context)

@login_required
def eliminarAgendamiento(request, consulta_id):
    consulta = get_object_or_404(Agendamiento, id=consulta_id)
    
    # Verificar si el usuario autenticado es el propietario del agendamiento
    if request.user == consulta.cliente:
        # Agregar mensaje de confirmación antes de eliminar
        messages.info(request, 'Se ha eliminado el agendamiento')
        consulta.delete()
    
    return redirect('app_clinica:historial_medico')  # Redirigir a la página del historial médico después de eliminar

@login_required
def editarAgendamiento(request, consulta_id):
    agendamiento = Agendamiento.objects.get(id=consulta_id)

    if request.method == 'POST':
        form = EditarAgendamientoForm(request.POST, instance=agendamiento, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamiento modificado exitosamente.')
            return redirect('/historial-medico/')
        else:
            print(form.errors)  # Imprimir los errores de validación del formulario
    else:
        form = EditarAgendamientoForm(instance=agendamiento, request=request)
        form.fields['agenda'].queryset = Agenda.objects.filter(categoria=agendamiento.categoria)

    print(form.errors)  # Imprimir los errores de validación del formulario antes de renderearlo

    context = {
        'form': form
    }
    return render(request, 'app/editar_agendamiento.html', context)

@login_required
def mascotaCliente(request):
    cliente = request.user.cliente
    mascotas = Mascota.objects.filter(dueno=cliente)
    context = {'mascotas': mascotas}
    return render(request, 'app/mascota_cliente.html', context)

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de la mascota se han actualizado correctamente.')
            return redirect('/tus-mascotas/', mascota_id=mascota.id)
        else:
            messages.error(request, 'No se pudieron actualizar los datos de la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = MascotaForm(instance=mascota)

    form.fields['fech_naci'].widget.attrs['value'] = mascota.fech_naci.strftime('%Y-%m-%d')

    return render(request, 'app/mascota/editar_mascota.html', {'form': form})

@login_required
def generar_pdf(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    diagnosticos = Diagnostico.objects.filter(agendamiento__mascota=mascota).select_related('agendamiento__categoria')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)

    elements = []
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_contenido = styles['BodyText']

    titulo = f'Ficha de mascota - {mascota.nombre.capitalize()}'
    elements.append(Paragraph(titulo, estilo_titulo))
    elements.append(Spacer(1, 0.5*inch))

    ruta_imagen = 'app_clinica/static/app/img/LogoPetCare.png'
    imagen = Image(ruta_imagen, width=2*inch, height=2*inch)
    elements.append(imagen)
    elements.append(Spacer(1, 0.5*inch))

    dueno_nombre = f'Dueño: {mascota.dueno.user.first_name.capitalize()} {mascota.dueno.user.last_name.capitalize()}'
    especie = f'Especie: {mascota.especie}'
    raza = f'Raza: {mascota.raza}'
    sexo = f'Sexo: {mascota.get_sexo_display()}'
    fecha_nacimiento = f'Fecha de Nacimiento: {mascota.fech_naci}'
    microchip = f'Microchip: {mascota.microchip}'

    elements.append(Paragraph(dueno_nombre, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(especie, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(raza, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(sexo, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(fecha_nacimiento, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(microchip, estilo_contenido))
    elements.append(Spacer(1, 0.5*inch))

    elements.append(Paragraph("Diagnósticos:", estilo_titulo))
    for diagnostico in diagnosticos:
        agendamiento = diagnostico.agendamiento
        categoria = agendamiento.categoria

        fecha_agendamiento = agendamiento.agenda.dia.strftime('%d/%m/%Y')
        nombre_veterinario = agendamiento.agenda.veterinario.user.get_full_name()

        elements.append(Spacer(1, 0.25*inch))
        elements.append(Paragraph(f"Fecha de Agendamiento: {fecha_agendamiento}", estilo_contenido))
        elements.append(Paragraph(f"Categoría: {categoria.nombre}", estilo_contenido))
        elements.append(Paragraph(f"Veterinario: {nombre_veterinario.title()}", estilo_contenido))
        elements.append(Spacer(1, 0.25*inch))
        elements.append(Paragraph(f"Diagnóstico: {diagnostico.diagnostico.capitalize()}", estilo_contenido))

    doc.build(elements)

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'Ficha-{mascota.nombre.capitalize()}.pdf')

@login_required
def agregarMascota(request):
    if request.method == 'POST':
        form = AgregarMascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueno = request.user.cliente
            mascota.save()
            messages.success(request, 'La mascota se ha guardado correctamente.')
            return redirect('/tus-mascotas/')
        else:
            messages.error(request, 'No se pudo guardar la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = AgregarMascotaForm()
    
    context = {'form': form}
    return render(request, 'app/mascota/agregar_mascota.html', context)

@login_required
def editarPerfil(request):
    cliente = request.user.cliente

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            user = form.instance.user
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            user.save()
            form.save()
            messages.success(request, 'Los cambios se guardaron correctamente.')
            return redirect('app_clinica:user')
        else:
            messages.error(request, 'Hubo un error al guardar los cambios. Por favor, verifica los datos ingresados.')
            print(form.errors)
    else:
        nombre = cliente.user.first_name
        apellido = cliente.user.last_name
        form = ClienteForm(instance=cliente, initial={'nombre': nombre, 'apellido': apellido})
        form.fields['fecha_nac'].widget = DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'birth-date', 'required': 'true'}, format='%Y-%m-%d')

    context = {'form': form}
    return render(request, 'app/editar_perfil.html', context)

@login_required
def editarPassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualizar la sesión del usuario para evitar cierre de sesión
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('app_clinica:user')
        else:
            messages.error(request, 'Hubo un error al cambiar la contraseña. Por favor, verifica los datos ingresados.')
    else:
        form = ChangePasswordForm(request.user)

    context = {'form': form}
    return render(request, 'app/change_password.html', context)


# Seccion solo para colaboradores
def colaborador_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        # Verificar si el usuario es válido y pertenece a uno de los grupos permitidos
        if user is not None and (Group.objects.filter(user=user, name='Colaboradores').exists() or 
                                 Group.objects.filter(user=user, name='Veterinarios').exists()):
            login(request, user)
            return redirect('app_clinica:colaborador')  # Redirige a la página de inicio del colaborador
        else:
            # Manejar error de inicio de sesión
            messages.error(request, 'Credenciales inválidas o usuario no es colaborador')
            return redirect('app_clinica:colaborador_login')  # Redirige al formulario de inicio de sesión
    else:
        return render(request, 'app/colaboradores/colaborador_login.html')

def is_veterinario(user):
    return user.groups.filter(name='Veterinarios').exists()

def is_veterinario_o_colaborador(user):
    return user.groups.filter(name__in=['Veterinarios', 'Colaboradores']).exists()

@login_required
def colaborador(request):
    user = request.user
    is_veterinario = user.groups.filter(name='Veterinarios').exists()
    is_colaborador = user.groups.filter(name='Colaboradores').exists()

    context = {
        'is_veterinario': is_veterinario,
        'is_colaborador': is_colaborador,
    }
    print(is_veterinario)
    return render(request, "app/colaboradores/dashboard_colaborador.html", context)

def obtener_horario(horario):
    horarios = dict(Agenda.HORARIOS)
    return horarios.get(horario)

import smtplib
from email.mime.text import MIMEText
@login_required
def enviar_correo(request, agendamiento_id):
    agendamiento = Agendamiento.objects.get(id=agendamiento_id)
    cliente = agendamiento.mascota.dueno
    dia_agendamiento = agendamiento.agenda.dia
    horario_agendamiento = agendamiento.agenda.get_horario_display()

    # Construir el mensaje de correo electrónico
    mensaje = f"""
    Estimado {cliente.user.get_full_name().title()},

    ¡Gracias por confiar en PetCare para el cuidado de su mascota!

    Le recordamos que tiene una cita programada para el día {dia_agendamiento} a las {horario_agendamiento} con el doctor {agendamiento.agenda.veterinario.user.get_full_name().title()}.

    Nos complace poder atenderle y brindarle el mejor servicio para el bienestar de su mascota. Si tiene alguna pregunta o necesita realizar alguna modificación, no dude en contactarnos.

    ¡Esperamos verlos pronto en nuestras instalaciones!

    Saludos cordiales,
    El equipo de PetCare
    """

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('petcarevetter@gmail.com', 'tsbnnvdijldznurx')

        msg = MIMEText(mensaje)
        msg['Subject'] = 'Recordatorio de Cita'
        msg['From'] = 'petcarevetter@gmail.com'
        msg['To'] = cliente.user.email

        server.send_message(msg)
        server.quit()

        messages.success(request, 'Correo electrónico enviado con éxito.')
        return redirect('app_clinica:recordatorio')
        

    except Exception as e:
        # Manejar cualquier error que ocurra durante el envío del correo electrónico
        messages.error(request, 'Error al enviar el correo electrónico.')
        return redirect('app_clinica:recordatorio') 

@login_required
def recordatorio(request):
    agendamientos = Agendamiento.objects.order_by('-agenda__dia')
    user = request.user
    is_colaborador = user.groups.filter(name='Colaboradores').exists()

    context = {
        'agendamientos': agendamientos,
        'is_colaborador': is_colaborador,
        'obtener_horario': obtener_horario,
    }
    return render(request, 'app/colaboradores/recordatorio.html', context)

@login_required
def editar_agendamiento(request, agendamiento_id):
    agendamiento = get_object_or_404(Agendamiento, id=agendamiento_id)
    user = request.user
    is_colaborador = user.groups.filter(name='Colaboradores').exists()

    if request.method == 'POST':
        form = EditAgendamientoColaborador(request.POST, instance=agendamiento)
        if form.is_valid():
            form.save()
            return redirect('app_clinica:recordatorio')
    else:
        form = EditAgendamientoColaborador(instance=agendamiento)

    form.request = request  # Agregar el objeto request al formulario

    context = {
        'form': form,
        'agendamiento': agendamiento,
        'is_colaborador': is_colaborador,
    }

    return render(request, 'app/colaboradores/editar_agendamiento.html', context)

@login_required
def buscar_clientes(request):
    query = request.GET.get('q')

    if query:
        clientes = Cliente.objects.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query),
            user__groups__isnull=True
        ).order_by('user__first_name', 'user__last_name')
    else:
        clientes = Cliente.objects.filter(user__groups__isnull=True).order_by(Upper('user__first_name'), Upper('user__last_name'))

    user = request.user
    is_colaborador = user.groups.filter(name='Colaboradores').exists()
    is_veterinario = user.groups.filter(name='Veterinarios').exists()

    context = {
        'clientes': clientes,
        'is_colaborador': is_colaborador,
        'is_veterinario': is_veterinario,
    }

    return render(request, 'app/colaboradores/buscar_clientes.html', context)

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    nombre_cliente = cliente.user.get_full_name()

    user = request.user
    is_colaborador = user.groups.filter(name='Colaboradores').exists()
    is_veterinario = user.groups.filter(name='Veterinarios').exists()

    context = {
        'is_colaborador': is_colaborador,
        'is_veterinario': is_veterinario,
    }
    
    if request.method == 'POST':
        form = EditarClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'El cliente {nombre_cliente.title()} se ha editado correctamente.')
            return redirect('app_clinica:buscar_clientes')
    else:
        form = EditarClienteForm(instance=cliente)
    
    context['form'] = form
    context['cliente'] = cliente
    context['nombre_cliente'] = nombre_cliente
    
    return render(request, 'app/colaboradores/editar_cliente.html', context)


# Seccion solo para veterinarios

@login_required
def citasColaborador(request):
    veterinario = request.user.veterinario  # Obtener el veterinario actualmente logeado
    agendamientos = Agendamiento.objects.select_related('mascota', 'categoria', 'agenda').filter(agenda__veterinario=veterinario)

    for agendamiento in agendamientos:
        agendamiento.tiene_diagnostico = agendamiento.diagnostico_set.exists()

    is_veterinario = request.user.groups.filter(name='Veterinarios').exists()
    context = {
        'agendamientos': agendamientos,
        'is_veterinario': is_veterinario
    }
    return render(request, "app/colaboradores/citas_colaborador.html", context)

@login_required
@user_passes_test(is_veterinario)
def diagnostico(request, consulta_id):
    agendamiento = Agendamiento.objects.get(id=consulta_id)

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico_text = form.cleaned_data['diagnostico']
            veterinario = request.user
            
            diagnostico = Diagnostico(agendamiento=agendamiento, diagnostico=diagnostico_text, veterinario=veterinario)
            diagnostico.save()
            
            messages.success(request, 'El diagnóstico se guardó correctamente.')
            
            return redirect('/citas-colaborador/')
            
    else:
        form = DiagnosticoForm()

    is_veterinario = request.user.groups.filter(name='Veterinarios').exists()
    context = {
        'agendamiento': agendamiento,
        'form': form,
        'is_veterinario': is_veterinario
    }
    return render(request, 'app/colaboradores/diagnostico.html', context)




































