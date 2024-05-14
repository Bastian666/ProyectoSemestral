from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ProductoForm
from .models import Productos

# Create your views here.

def home(request):
    return render(request, 'home.html')


def registro (request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return HttpResponse('Usuario creado correctamente')
            except IntegrityError:
                return render(request, 'registro.html', {
                'form': UserCreationForm,
                "error": 'El usuario ya existe'
                })
        return render(request, 'registro.html', {
                'form': UserCreationForm,
                "error": 'Las contraseñas no coinciden'
                })
    
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
            return render(request, 'ingresar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  
         
        if user is None:
            return render(request, 'ingresar.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrectos'
        })
        else:
            login(request, user)
            return redirect('home')
        
def agregarProd(request):

    if request.method == 'GET':
            return render(request, 'agregarProd.html', {
        'form': ProductoForm
    })
    else:
        try:
         form = ProductoForm(request.POST, request.FILES)
         nuevo_producto = form.save(commit=False)
         nuevo_producto.user = request.user
         nuevo_producto.save()
         return redirect('home')
        except ValueError:
            return render(request, 'agregarProd.html', {
                'form' : ProductoForm,
                'error': 'Ingrese información valida'
            })

def productos(request):
    productos = Productos.objects.all()

    return render(request, 'productos.html', {'productos': productos})

def detalleProd(request, producto_id):
    if request.method == 'GET':
        producto = get_object_or_404(Productos, pk=producto_id)
        form = ProductoForm(instance=producto)
        return render(request, 'detalleProd.html', {'producto': producto, 'form' : form})
    else:
        try:
            producto = get_object_or_404(Productos, pk=producto_id)
            form = ProductoForm(request.POST, instance=producto)
            form.save()
            return redirect('productos')
        except ValueError:
            return render(request, 'detalleProd.html', {'producto': producto, 'form': form,
            'error': "Error al actualizar el producto"})
        
def eliminarProd(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')

