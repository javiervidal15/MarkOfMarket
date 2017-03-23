from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import  render

from appmark.models import Mercado,Moneda,Cambio
from urllib.request import urlopen
import json

def Index(request):
    mercados = Mercado.objects.all()
    return render(request=request,template_name='index.html',context={'mercados': mercados})

def ActualizarMercados(request):
    poloniex = Mercado.objects.get(nombre = 'Poloniex')
    bittrex = Mercado.objects.get(nombre = 'Bittrex')
    #kraken = Mercado.objects.get(nombre = 'Kraken')

    stringbittrex = urlopen('https://bittrex.com/api/v1.1/public/getmarkets').read().decode('utf-8')
    jsonbittrex = json.loads(stringbittrex)

    stringpoloniex = urlopen('https://poloniex.com/public?command=returnTicker').read().decode('utf-8')
    jsonpoloniex = json.loads(stringpoloniex)

    #jsonkraken = json.load(urllib2.urlopen(kraken.url))

    for i in jsonbittrex['result']:
        destino = str(i['MarketCurrency'])
        base = str(i['BaseCurrency'])
        verificarMercado(base,destino,bittrex)

    for i in jsonpoloniex:
        destino = str(i).split('_')[1]
        base = str(i).split('_')[0]
        verificarMercado(base,destino,poloniex)

    # for i in jsonkraken['result']:
    #     destino = jsonkraken['result'][i]['altname']
    #     base = 'BTC'
    #     verificarMercado(base,destino,kraken)

    return HttpResponseRedirect(reverse('index'))


def verificarMercado(base,destino,mercado):
    cambio = verificarCambio(base,destino)
    if not Mercado.objects.filter(nombre = mercado.nombre,cambios=cambio):
        mercado.cambios.add(cambio)


def verificarCambio(base,destino):
    mbase = verificarMoneda(base)
    mdestino = verificarMoneda(destino)
    cambio = Cambio.objects.filter(monedabase=mbase,monedadestino=mdestino)

    if not cambio:
        cambio = Cambio(monedabase=mbase,monedadestino=mdestino)
        cambio.save()
    else:
        cambio = cambio.first()

    return cambio


def verificarMoneda(base):
    aux = Moneda.objects.filter(nombre=base)
    if not aux :
        aux = Moneda(nombre=base)
        aux.save()
    else:
        aux = aux.first()

    return aux