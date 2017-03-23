from __future__ import unicode_literals
from django.db import models


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
    cambios = models.ManyToManyField('Cambio',blank=True)

    def get_nombre(self):
        return self.nombre

    def get_cambios(self):
        return self.cambios

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

class Registro(models.Model):
    cambio = models.ForeignKey(Cambio)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.FloatField()
    




