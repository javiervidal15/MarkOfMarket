from django.contrib import admin

from appmark.models import Mercado, Cambio, Moneda, Registro

admin.site.register(Mercado)
admin.site.register(Cambio)
admin.site.register(Moneda)
admin.site.register(Registro)

