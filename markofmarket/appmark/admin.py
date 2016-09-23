from django.contrib import admin
from models import Mercado
# Register your models here.
class MercadoAdmin(admin.ModelAdmin):

        list_display = ('nombre',)
admin.site.register(Mercado,MercadoAdmin)
