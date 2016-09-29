from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.

class Moneda(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):

        return self.nombre

    def __unicode__(self):

        return self.nombre


class Cambio(models.Model):
    monedabase = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='base')
    monedadestino = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='destino')

    def __str__(self):

        return  '%s-%s'  %(self.monedabase,self.monedadestino)

class Mercado(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.URLField()
    cambios = models.ManyToManyField('Cambio',blank=True)

    def __str__(self):

        return self.nombre

    def __unicode__(self):
        return self.nombre





