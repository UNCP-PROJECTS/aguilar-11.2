from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'creado_en')
    list_filter = ('categoria', 'creado_en')
    search_fields = ('nombre', 'descripcion', 'categoria')
    ordering = ('-creado_en',)
