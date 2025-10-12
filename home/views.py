#redirect es para redirigir a otra pagina
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #biblioteca crea registros de usuarios // loguea usuarios
from django.contrib.auth.models import User #creacion de usuario
from django.http import HttpResponse #para devolver respuestas http
from django.contrib.auth import login,logout, authenticate #para guardar los registros de sesion del usuario(coockies) // cerrar sesion // autentificar, corroborar los datos y loguear
from django.db import IntegrityError #para manejar errores de integridad
# Create your views here.
def home (request):
    return render(request,'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request,'signup.html',{ 
        'form':UserCreationForm #instancia del formulario, tambien debe estar en el html
        })   
    else: #es decir si es POST
        if request.POST['password1'] == request.POST['password2']: #si una contraseña es igual a la otra
            
            try: #intenta crear el usuario
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1']) #creamos el usuario
                user.save() #guardamos el usuario en la base de datos
                login(request,user) #iniciamos sesion
                return redirect('inventario') #redireccionamos a la pagina de inventario
            except IntegrityError: #si hay un error de integridad, es decir, si el usuario ya existe
                return render(request,'signup.html',{
                'form':UserCreationForm, #instancia del formulario, tambien debe estar en el html
                'error': 'Usuario ya existe'
        })   
        return render(request,'signup.html',{
        'form':UserCreationForm, #instancia del formulario, tambien debe estar en el html
        'error': 'Las contraseñas no coinciden'
        })   
        
def signout(request):
    logout(request) #cerramos sesion
    return redirect('home') #redireccionamos a la pagina de inicio

def signin(request):
    if request.method == 'GET': #si es get. envía la pagina
        return render(request, 'signin.html',{ 
            'form': AuthenticationForm
        })
    else: #si es POST recibimos los datos que coloca el usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']) #verifica usuario y contraseña que coloca el usuario con el que tenemos en la base de datos
        if user is None: #si no encuentra alguno de los dos datos, retornamos la pagina con un mensaje de error
            return render(request, 'signin.html',{ #nos envia a la pagina
            'form': AuthenticationForm, #nos muestra el formulario
            'error': 'Usuario o contraseña incorrectos ' #nos muestra mensaje de error
        })
        else:
            login(request,user) #loguea al usuario
            return redirect('inventario')  #nos envia al inventario
            
    


def inventario(request):
    return render(request,'inventario.html')

