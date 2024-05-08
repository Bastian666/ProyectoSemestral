from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    fechaCreado = models.DateTimeField(auto_now_add=True)
    fechaIngreso = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre + '- by ' + self.user.username
