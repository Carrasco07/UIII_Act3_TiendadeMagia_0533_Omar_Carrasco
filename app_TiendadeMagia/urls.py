from django.urls import path
from . import views

# =========================================================================
# CONFIGURACIÓN DE URLS DE LA APLICACIÓN (CORREGIDA)
# =========================================================================

urlpatterns = [
    # URL de Inicio
    path('', views.inicio_TiendadeMagia, name='inicio_TiendadeMagia'),

    # CRUD para Producto 
    path('productos/', views.ver_producto, name='ver_producto'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    
    # Mostrar formulario de actualización (GET)
    # *** CAMBIO CLAVE: Usamos 'editar_producto' como nombre ***
    path('productos/actualizar/<int:producto_id>/', 
         views.actualizar_producto, 
         name='editar_producto'),
         
    # Procesar la actualización (POST) - Mantenemos el nombre original
    path('productos/actualizar/realizar/<int:producto_id>/', 
         views.realizar_actualizacion_producto, 
         name='realizar_actualizacion_producto'),
         
    # Borrar producto
    # *** CAMBIO CLAVE: Usamos 'eliminar_producto' como nombre ***
    path('productos/borrar/<int:producto_id>/', 
         views.borrar_producto, 
         name='eliminar_producto'),

    # NOTA: Debes agregar aquí las URLs para OrdenesDeVenta y DetalleOrden si no lo has hecho
]