from django.contrib import admin
from .models import Productos

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaCreado", )

# Register your models here.
admin.site.register(Productos)