from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .Formulario import FormularioEventos, FormularioInscripcion
from .models import Eventos, Inscripciones
# Create your views here.


def RegistrarUsuario(request):
    
    if request.method == "POST":
        
        try:
            
            nombre = request.POST.get("txtNombre")
            correoEmail = request.POST.get("txtEmail")
            clave = request.POST.get("txtClave")
            
            Usuario = User(username=nombre, email=correoEmail)
            Usuario.set_password(clave)
            
            Usuario.save()
            login(request,Usuario)
            
            return redirect('RegistroUsuario')
        
        except:
            
            return render(request, "Registro.html", {"error":"El usuario ya existe"})
    

    
    return render(request, "Registro.html")

def LogearUsuario(request):
    
    
    if request.method == "POST":
        usuario = request.POST.get("txtUsuario")
        clave = request.POST.get("txtClave")
        
        print(f"Usuario: {usuario}, Clave: {clave}")
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            print("Autenticación exitosa")
            login(request, user)
            return redirect("DetalleEventos")
        else:
            print("Autenticación fallida")
            return render(request, "Login.html", {"error": "El usuario o la clave no existen"})
    
    return render(request, "Login.html")


def CrearEvento(request):
    
    
    if request.method == "POST":
        
        formulario = FormularioEventos(request.POST)
        
        if formulario.is_valid():
            evento = formulario.save(commit=False)
            evento.usuario = request.user
            formulario.save()
            formulario.save_m2m()
            
            
            participantes = request.POST.getlist('participantes')
            
            for participante_id in participantes:
                usuario = User.objects.get(id=participante_id)
                Inscripciones.objects.create(idEvento=evento, usuario = usuario)
            
            return redirect('DetalleEventos')
        else:
            return render(request, "CrearEventos.html", {"Formulario": formulario, "Error": "Error al validar el formulario"})
    
    else:
        
        formulario = FormularioEventos()
        
    
    return render(request, "CrearEventos.html", {"Formulario": formulario})


def detalleEventos(request):
    
    if request.user.is_authenticated:
        eventosObtenidos = Eventos.objects.filter(usuario=request.user)
    
    else:
        eventosObtenidos = []
    
    return render(request, "EventosCreados.html", {"eventos": eventosObtenidos})


def CerrarSesion(request):
    
    logout(request)
    
    return redirect('LoginUsuario')


def EditarEvento(request, idEvento):
    
    evento = get_object_or_404(Eventos, pk=idEvento)
    formulario = FormularioEventos(request.POST)
    inscripciones = Inscripciones.objects.filter(idEvento=evento)
    
    if request.method == "POST":
        
        formulario = FormularioEventos(request.POST,instance=evento)
        formulario_inscripcion = FormularioInscripcion(request.POST)
        if formulario.is_valid() and formulario_inscripcion.is_valid:
            
            evento = formulario.save() 
            inscripcion = formulario_inscripcion.save(commit=False)
            inscripcion.idEvento = evento
            inscripcion.save()
            
            return redirect('DetalleEventos')
        else:
            
            return render(request, "AgregarMasParticipantes.html", {
                "error_evento": "Error al editar el evento",
                "error_participantes": "Error al editar participantes",
                "formulario_evento": formulario,
                "formulario_inscripcion": formulario_inscripcion,
                "evento": evento,
                "inscripciones": inscripciones
            })
    else:
        
        formulario = FormularioEventos(instance=evento)
        formulario_inscripcion = FormularioInscripcion()
    
    return render(request, "AgregarMasParticipantes.html", {
        "formulario_evento": formulario,
        "formulario_inscripcion": formulario_inscripcion,
        "evento": evento,
        "inscripciones": inscripciones
    })