__author__ = 'javie'

from models import Mercado
from models import Cambio
from models import Moneda

def verificarMercado(base,destino,mercado):
    cambio = verificarCambio(base,destino)
    if not Mercado.objects.filter(nombre = mercado.nombre,cambios=cambio):
        mercado.cambios.add(cambio)


def verificarMoneda(base):
    aux = Moneda.objects.filter(nombre=base)
    if not aux :
        aux = Moneda(nombre=base)
        aux.save()
    else:
        aux = aux[0]

    return aux

def verificarCambio(base,destino):
    mbase = verificarMoneda(base)
    mdestino = verificarMoneda(destino)
    cambio = Cambio.objects.filter(monedabase=mbase,monedadestino=mdestino)

    if not cambio:
        cambio = Cambio(monedabase=mbase,monedadestino=mdestino)
        cambio.save()
    else:
        cambio = cambio[0]

    return cambio