from django.db import models
from django.core.validators import MinValueValidator

# =========================================================================
# 1. MODELO PRODUCTO
# =========================================================================

class Producto(models.Model):
    # Opciones de Categoría predefinidas
    CATEGORIA_CHOICES = [
        ('Pociones', 'Pociones'),
        ('Artefactos', 'Artefactos'),
        ('Hechizos', 'Hechizos'),
        ('Ingredientes', 'Ingredientes'),
        ('Otros', 'Otros'),
    ]

    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nombre del Artículo"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción Mágica"
    )
    categoria = models.CharField(
        max_length=50, 
        choices=CATEGORIA_CHOICES, 
        default='Otros'
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio (USD)"
    )
    stock = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Cantidad en Inventario"
    )
    proveedor = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Proveedor Místico"
    )
    fecha_ingreso = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Ingreso"
    )

    class Meta:
        verbose_name = "Producto Mágico"
        verbose_name_plural = "Productos Mágicos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

# =========================================================================
# 2. MODELO ORDEN DE VENTA
# =========================================================================

class OrdenDeVenta(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Procesando', 'Procesando'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]
    METODO_CHOICES = [
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia Bancaria'),
        ('Cripto', 'Criptomoneda Arcana'),
    ]

    cliente = models.CharField(
        max_length=255, 
        verbose_name="Nombre del Cliente"
    )
    fecha_orden = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de la Orden"
    )
    direccion_envio = models.TextField(
        verbose_name="Dirección de Envío"
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Monto Total"
    )
    estado = models.CharField(
        max_length=50, 
        choices=ESTADO_CHOICES, 
        default='Pendiente'
    )
    metodo_pago = models.CharField(
        max_length=50, 
        choices=METODO_CHOICES, 
        default='Tarjeta',
        verbose_name="Método de Pago"
    )

    class Meta:
        verbose_name = "Orden de Venta"
        verbose_name_plural = "Órdenes de Venta"
        ordering = ['-fecha_orden']

    def __str__(self):
        return f"Orden #{self.id} - Cliente: {self.cliente}"

# =========================================================================
# 3. MODELO DETALLE DE ORDEN (Líneas de la Orden)
# =========================================================================

class DetalleOrden(models.Model):
    # Relación uno a muchos con OrdenDeVenta
    orden = models.ForeignKey(
        OrdenDeVenta, 
        related_name='detalles', 
        on_delete=models.CASCADE,
        verbose_name="Orden Asociada"
    )
    # Relación uno a muchos con Producto
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.RESTRICT, # No permite borrar un producto si tiene detalles de orden
        verbose_name="Producto"
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad Comprada"
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio Unitario al Comprar"
    )

    class Meta:
        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalles de Órdenes"
        # Asegura que no se duplique la misma línea de producto en la misma orden
        unique_together = ('orden', 'producto')

    def subtotal(self):
        """Calcula el subtotal de esta línea de la orden."""
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Detalle de Orden #{self.orden.id}: {self.cantidad} x {self.producto.nombre}"