from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=50, default="General")
    stock = models.IntegerField(default=0)
    precio = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    imagen = models.ImageField(upload_to='productos', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre + '- by ' + self.user.username
