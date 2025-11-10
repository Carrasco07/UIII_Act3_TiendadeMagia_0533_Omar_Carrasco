from django.contrib import admin
from .models import Producto, OrdenDeVenta, DetalleOrden

# =========================================================================
# REGISTRO DE MODELOS (Paso 27)
# =========================================================================

# 1. Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'proveedor', 'fecha_ingreso')
    search_fields = ('nombre', 'categoria', 'proveedor')
    list_filter = ('categoria', 'proveedor', 'fecha_ingreso')
    list_editable = ('precio', 'stock')

# 2. DetalleOrden (Usado como inline para OrdenDeVenta)
class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1 # Cuántas líneas vacías para agregar detalles nuevos

# 3. OrdenDeVenta
@admin.register(OrdenDeVenta)
class OrdenDeVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_orden', 'total', 'estado', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha_orden')
    search_fields = ('cliente', 'direccion_envio')
    date_hierarchy = 'fecha_orden'
    inlines = [DetalleOrdenInline] # Permite agregar productos directamente desde la orden