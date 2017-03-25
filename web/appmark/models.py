from __future__ import unicode_literals
from django.db import models
from model_utils.managers import InheritanceManager


class Moneda(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class Cambio(models.Model):
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    monedabase = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='base')
    monedadestino = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='destino')

    def get_monedabase(self):
        return self.monedabase

    def get_monedadestino(self):
        return self.monedadestino

    def __str__(self):
        return  '%s-%s'  %(self.monedabase,self.monedadestino)

class Mercado(models.Model):
    nombre = models.CharField(max_length=50)
    cambios = models.ManyToManyField('Cambio',blank=True)

    def get_nombre(self):
        return self.nombre

    def get_cambios(self):
        return self.cambios

    def get_cambios_dic(self):
        dic = {}
        for cambio in self.get_cambios().all():
            dic[str(cambio)] = cambio
        return dic

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

class Registro(models.Model):
    cambio = models.ForeignKey(Cambio)
    mercado = models.ForeignKey(Mercado)
    fecha = models.DateTimeField(auto_now_add=True)
    #last
    last = models.FloatField()
    #highestBid and Bid
    highest_bid = models.FloatField()
    #lowestAsk and ask
    lowest_ask = models.FloatField()
    #baseVolume
    base_volume = models.FloatField()
    #quoteVolume and volume
    quote_volume = models.FloatField()
    #high24hr and high
    high_24hr = models.FloatField()
    #low24hr and low
    low_24hr = models.FloatField()
    #Just bittrex
    open_buy_orders = models.FloatField(default=0)
    # Just bittrex
    open_shell_orders = models.FloatField(default=0)

    def __str__(self):
        return "%s:%s:%s - %s " %(self.mercado, self.cambio,self.last, self.fecha)

    def get_fecha(self):
        return self.fecha

    def get_mercado(self):
        return self.mercado

    def get_cambio(self):
        return self.cambio

    def get_last(self):
        return self.last

    def get_highest_bid(self):
        return self.highest_bid

    def get_lowest_ask(self):
        return self.lowest_ask

    def get_base_volume(self):
        return self.base_volume

    def get_quote_volume(self):
        return self.quote_volume

    def get_high24hr(self):
        return self.high_24hr

    def get_low24hr(self):
        return self.low_24hr

    def get_open_buy_orders(self):
        return self.open_buy_orders

    def get_open_shell_orders(self):
        return self.open_shell_orders