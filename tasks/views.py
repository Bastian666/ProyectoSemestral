from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ProductoForm
from .models import Productos
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Carrito, ItemCarrito
import requests

# Create your views here.

def home(request):
    productos = Productos.objects.all()  # Obtén todos los productos
    return render(request, 'home.html', {'productos': productos})

#REGISTRARSE EN EL SISTEMA
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
                return redirect('home')
            except IntegrityError:
                return render(request, 'registro.html', {
                'form': UserCreationForm,
                "error": 'El usuario ya existe'
                })
        return render(request, 'registro.html', {
                'form': UserCreationForm,
                "error": 'Las contraseñas no coinciden'
                })

#SALIR DE LA SESIÓN
@login_required 
def signout(request):
    logout(request)
    return redirect('home')

#INICIAR SESIÓN
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

@login_required
def agregarProd(request):
    if request.user.username != "admin":
        # Si el usuario no es "admin", redirigirlo a la página de inicio ('home')
        return redirect('home')

    if request.method == 'GET':
        return render(request, 'agregarProd.html', {
            'form': ProductoForm()
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
                'form': ProductoForm(),
                'error': 'Ingrese información válida'
            })

@login_required
def productos(request):
    productos = Productos.objects.all()
    if request.user.username == "admin":
        return render(request, "productos.html", {"productos": productos})
    else:
        return render(request, "productosUser.html", {"productos": productos})


@login_required
def detalleProd(request, producto_id):
    if request.user.username != "admin":
        # Si el usuario no es "admin", redirigirlo a la página de inicio ('home')
        return redirect('home')

    producto = get_object_or_404(Productos, pk=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            nuevo_stock = form.cleaned_data['stock']
            if nuevo_stock >= 0:
                form.save()
                return redirect('productos')
            else:
                return render(request, 'detalleProd.html', {
                    'producto': producto,
                    'form': form,
                    'error': "El stock no puede ser menor que cero."
                })
        else:
            return render(request, 'detalleProd.html', {
                'producto': producto,
                'form': form,
                'error': "Error en los datos del formulario."
            })

    else:
        form = ProductoForm(instance=producto)
        return render(request, 'detalleProd.html', {'producto': producto, 'form': form})


@login_required     
def eliminarProd(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if producto.stock > 0:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not item_created:
            item.cantidad += 1
        item.save()
        producto.stock -= 1
        producto.save()
    return redirect('productos')


@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all()
    total_real = sum(item.producto.precio * item.cantidad for item in items)
    
    # Calcular el IVA (19% del total real)
    iva = total_real * 0.19
    
    total_con_iva = total_real + iva
    
    return render(request, 'carrito.html', {'items': items, 'total_real': total_real, 'total_con_iva': total_con_iva, 'iva': iva})



@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id)
    producto = item.producto

    if item.cantidad > 1:
        # Eliminar una unidad
        item.cantidad -= 1
        item.save()
    else:
        # Eliminarlo por completo del carrito
        item.delete()

    # Redirigir a la página del carrito
    return redirect('carrito')


@login_required
def vaciar_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all()
    for item in items:
        item.producto.stock += item.cantidad
        item.producto.save()
        item.delete()  # Elimina cada item individualmente
    return redirect('carrito')

