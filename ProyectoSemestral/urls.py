from django.contrib import admin
from django.urls import path, include
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.signout, name='logout'),
    path('ingresar/', views.signin, name='ingresar'),
    path('agregarProd/', views.agregarProd, name='agregarProd'),
    path('productos/', views.productos, name='productos'),
    path('productos/<int:producto_id>/', views.detalleProd, name='detalleProd'),
    path('productos/<int:producto_id>/eliminar/', views.eliminarProd, name='eliminarProd'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/actualizar_stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),  
        path('favoritos/', views.favoritos, name='favoritos'),
         path('toggle_favorito/<int:producto_id>/', views.toggle_favorito, name='toggle_favorito'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
