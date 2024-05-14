# Generated by Django 5.0.4 on 2024-05-14 15:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_productos_fechacreado_productos_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productos',
            name='fechaCreado',
        ),
        migrations.RemoveField(
            model_name='productos',
            name='fechaIngreso',
        ),
        migrations.AddField(
            model_name='productos',
            name='categoria',
            field=models.CharField(default='General', max_length=50),
        ),
        migrations.AddField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(null=True, upload_to='productos'),
        ),
        migrations.AddField(
            model_name='productos',
            name='precio',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
