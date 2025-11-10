from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Producto, OrdenDeVenta, DetalleOrden # Importamos todos los modelos
from django.urls import reverse

# =========================================================================
# VISTAS GENERALES (Paso 14)
# =========================================================================

def inicio_TiendadeMagia(request):
    """Muestra la página de inicio del sistema."""
    return render(request, 'inicio.html', {
        'titulo': 'Sistema de Administración de Tienda de Magia'
    })

# =========================================================================
# VISTAS CRUD DE PRODUCTO (Paso 14, 23, 27)
# Se usa request.POST directamente (Paso 23: No utilizar forms.py)
# =========================================================================

def ver_producto(request):
    """Muestra la lista de todos los productos en una tabla."""
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'producto/ver_producto.html', {
        'productos': productos,
        'titulo': 'Ver Productos'
    })

def agregar_producto(request):
    if request.method == 'POST':
        # Extracción manual de datos
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        fecha_registro = request.POST.get('fecha_registro') # <--- CAMPO AÑADIDO
        
        try:
            # Validación y conversión
            precio = float(precio)
            stock = int(stock)

            # Crear y guardar el objeto
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                fecha_registro=fecha_registro # <--- ASIGNACIÓN DE LA FECHA
            )
            return redirect('ver_producto')
        except ValueError:
            return render(request, 'producto/agregar_producto.html', {
                'error': 'El precio y el stock deben ser números válidos.',
                'titulo': 'Agregar Producto'
            })
            
    # Para GET: Inicializa la vista
    return render(request, 'producto/agregar_producto.html', {
        'titulo': 'Agregar Producto'
    })

def actualizar_producto(request, producto_id):
    """Muestra el formulario prellenado para editar un producto."""
    # Obtenemos el objeto o devolvemos un 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)
    
    return render(request, 'producto/actualizar_producto.html', {
        'producto': producto,
        'titulo': 'Actualizar Producto'
    })

def realizar_actualizacion_producto(request, producto_id):
    """Maneja la lógica del POST para actualizar el producto."""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        
        try:
            # Actualización de los campos
            producto.nombre = request.POST['nombre']
            producto.descripcion = request.POST['descripcion']
            producto.categoria = request.POST['categoria']
            producto.precio = request.POST['precio']
            producto.proveedor = request.POST['proveedor']
            producto.stock = request.POST.get('stock', producto.stock) # Usa el valor actual si no se proporciona
            
            producto.save()
            
            # Redirigir a la lista de productos
            return redirect('ver_producto')
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            # Volver al formulario con el producto y un mensaje de error
            return render(request, 'producto/actualizar_producto.html', {
                'producto': producto,
                'error_message': 'Hubo un error al actualizar el producto.',
                'titulo': 'Actualizar Producto'
            })
    
    # Si no es POST, redirigir al formulario de edición (debería ser GET)
    return redirect('ver_producto')


def borrar_producto(request, producto_id):
    """
    Muestra la página de confirmación de borrado y maneja la eliminación.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        # Si se confirma la eliminación
        try:
            producto.delete()
            return redirect('ver_producto')
        except Exception as e:
            # Si hay un error (ej. restricción de clave foránea)
            return render(request, 'producto/borrar_producto.html', {
                'producto': producto,
                'error_message': 'No se pudo eliminar el producto. Podría estar asociado a una Orden de Venta.',
                'titulo': 'Borrar Producto'
            })

    # Si es GET, muestra la página de confirmación
    return render(request, 'producto/borrar_producto.html', {
        'producto': producto,
        'titulo': 'Borrar Producto'
    })