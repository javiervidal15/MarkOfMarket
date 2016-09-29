from django.shortcuts import render_to_response

from models import Mercado
from verificaciones import verificarMercado
import urllib2
import json

# Create your views here.

def index(request,actualizar=False):


    poloniex = Mercado.objects.get(nombre = 'Poloniex')
    bittrex = Mercado.objects.get(nombre = 'Bittrex')
    kraken = Mercado.objects.get(nombre = 'Kraken')
    listamercados = Mercado.objects.all()
    listacambios = []
    if actualizar:

        jsonbittrex = json.load(urllib2.urlopen(bittrex.url))
        jsonpoloniex = json.load(urllib2.urlopen(poloniex.url))
        jsonkraken = json.load(urllib2.urlopen(kraken.url))

        for i in jsonbittrex['result']:
            destino = str(i['MarketCurrency'])
            base = str(i['BaseCurrency'])
            verificarMercado(base,destino,bittrex)

        for i in jsonkraken['result']:
            destino = jsonkraken['result'][i]['altname']
            base = 'BTC'
            verificarMercado(base,destino,kraken)

        for i in jsonpoloniex:
            destino = str(i).split('_')[1]
            base = str(i).split('_')[0]
            verificarMercado(base,destino,poloniex)



    return render_to_response('index.html',{'listamercados': listamercados, 'listacambios': listacambios})

