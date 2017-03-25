import csv
from time import time
from timeit import timeit

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import  render
from django.utils.timezone import now

from appmark.models import Mercado,Moneda,Cambio, Registro
from urllib.request import urlopen
import json

def Index(request):
    mercados = Mercado.objects.all()
    return render(request=request,template_name='index.html',context={'mercados': mercados})

def DescargarRegistros(request):
    registros = Registro.objects.all()

    # Creamos el objeto Httpresponse con la cabecera CSV apropiada.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clientes.csv'

    # Creamos un escritor CSV usando a HttpResponse como "fichero"
    writer = csv.writer(response)
    writer.writerow(['Fecha','Mercado', 'MonedaBase','MonedaDestino','Last','Highest bid','Lowest ask', 'Base volume','Quote volume',
                     'High 24hr','Low 24hr','Open buy orders', 'Open shell orders'])
    for reg in registros:
        writer.writerow([reg.get_fecha(),reg.get_mercado().id,reg.get_cambio().get_monedabase().id,
                         reg.get_cambio().get_monedadestino().id,reg.get_last(), reg.get_highest_bid(),reg.get_lowest_ask(),
                        reg.get_base_volume(),reg.get_quote_volume(),reg.get_high24hr(),reg.get_low24hr(),reg.get_open_buy_orders(),
                        reg.get_open_shell_orders()],)

    return response


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
    return cambio

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


def InsertarRegistros(request):
    tiempo_inicio = time()
    guardarRegistros()
    tiempo = time() - tiempo_inicio

    return render(request=request,template_name="index.html",context={'tiempo':tiempo})

def guardarRegistros():
    # Obtengo los mercados
    bittrex = Mercado.objects.get(nombre="Bittrex")
    poloniex = Mercado.objects.get(nombre="Poloniex")

    # Obtengo el diccionario de cambios de los mercados
    dic_bittrex = bittrex.get_cambios_dic()
    dic_poloniex = poloniex.get_cambios_dic()

    # Obtengo el json con la informacion de bittrex
    stringbittrex = urlopen('https://bittrex.com/api/v1.1/public/getmarketsummaries').read().decode('utf-8')
    jsonbittrex = json.loads(stringbittrex)

    # Obtengo el json con la informacion de poloniex
    stringpoloniex = urlopen('https://poloniex.com/public?command=returnTicker').read().decode('utf-8')
    jsonpoloniex = json.loads(stringpoloniex)

    # Obtengo fecha y hora actual
    fecha = now()

    registros = []
    for i in jsonbittrex['result']:
        market_name = str(i['MarketName'])

        if not market_name in dic_bittrex:
            destino = market_name.split('_')[1]
            base = market_name.split('_')[0]
            cambio = verificarMercado(base, destino, bittrex)
        else:
            cambio = dic_bittrex[market_name]

        last = str(i['Last'])
        highest_bid = str(i['Bid'])
        lowest_ask = str(i['Ask'])
        base_volume = str(i['BaseVolume'])
        quote_volume = str(i['Volume'])
        high_24hr = str(i['High'])
        low_24hr = str(i['Low'])
        open_buy_orders = str(i['OpenBuyOrders'])
        open_shell_orders = str(i['OpenSellOrders'])

        registros.append(Registro(cambio=cambio, mercado=bittrex, fecha=fecha, last=last, highest_bid=highest_bid,
                               lowest_ask=lowest_ask,
                               base_volume=base_volume, quote_volume=quote_volume, high_24hr=high_24hr,
                               low_24hr=low_24hr,
                               open_buy_orders=open_buy_orders, open_shell_orders=open_shell_orders))

    for i in jsonpoloniex:
        market_name = str(i)

        if not market_name in dic_poloniex:
            destino = market_name.split('_')[1]
            base = market_name.split('_')[0]
            cambio = verificarMercado(base, destino, poloniex)
        else :
            cambio = dic_poloniex[market_name]

        last = str(jsonpoloniex[market_name]['last'])
        highest_bid = str(jsonpoloniex[market_name]['highestBid'])
        lowest_ask = str(jsonpoloniex[market_name]['lowestAsk'])
        base_volume = str(jsonpoloniex[market_name]['baseVolume'])
        quote_volume = str(jsonpoloniex[market_name]['quoteVolume'])
        high_24hr = str(jsonpoloniex[market_name]['high24hr'])
        low_24hr = str(jsonpoloniex[market_name]['low24hr'])

        registros.append(Registro(cambio=cambio, mercado=poloniex, fecha=fecha, last=last, highest_bid=highest_bid,
                               lowest_ask=lowest_ask,
                               base_volume=base_volume, quote_volume=quote_volume, high_24hr=high_24hr,
                               low_24hr=low_24hr ))


    Registro.objects.bulk_create(registros)
