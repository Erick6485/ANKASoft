from sqlalchemy.orm import Session
from database import models
from datetime import datetime, timedelta
import random

# Datos realistas basados en el PDF de la hackatón
CATEGORIAS_MUJER = ["ABRIGO", "BERMUDA", "BUZOS", "CAMISAS", "FALDA", "JEANS TERMINADOS", "PANTALONES", "VESTIDOS"]
CATEGORIAS_HOMBRE = ["BERMUDA", "BUZO", "CAMISAS", "JEANS TERMINADOS", "PANTALONES", "POLOS", "TSHIRT TERMINADA"]
CATEGORIAS_NIÑO = ["BERMUDA", "BUZO", "CAMISAS", "JEANS TERMINADOS", "PANTALONES", "POLOS"]
CATEGORIAS_NIÑA = ["BERMUDA", "BUZO", "CAMISAS", "FALDA", "JEANS TERMINADOS", "VESTIDOS"]

TALLAS_ADULTOS = ["XXS", "XS", "S", "M", "L", "XL"]
TALLAS_NIÑOS = ["4", "6", "8", "10", "12", "14", "16"]

SUCURSALES = ["Sucursal Norte", "Sucursal Sur", "Sucursal Centro", "Sucursal Este"]

def crear_sucursales_ejemplo(db: Session):
    """Crear sucursales de ejemplo"""
    sucursales = [
        models.Sucursal(
            nombre="Sucursal Norte",
            ciudad="Ciudad Principal",
            direccion="Av. Principal 123",
            telefono="+57 123 456 7890"
        ),
        models.Sucursal(
            nombre="Sucursal Sur", 
            ciudad="Ciudad Principal",
            direccion="Calle Sur 456",
            telefono="+57 123 456 7891"
        ),
        models.Sucursal(
            nombre="Sucursal Centro",
            ciudad="Ciudad Principal", 
            direccion="Plaza Central 789",
            telefono="+57 123 456 7892"
        ),
        models.Sucursal(
            nombre="Sucursal Este",
            ciudad="Ciudad Secundaria",
            direccion="Av. Este 321",
            telefono="+57 123 456 7893"
        )
    ]
    
    db.add_all(sucursales)
    db.commit()
    print(f"✅ {len(sucursales)} sucursales creadas")
    return sucursales

def crear_productos_ejemplo(db: Session):
    """Crear productos de ejemplo basados en el portafolio del PDF"""
    productos = []
    
    # Productos para MUJER
    for categoria in CATEGORIAS_MUJER:
        for talla in TALLAS_ADULTOS:
            producto = models.Producto(
                nombre=f"{categoria.title()} Mujer Talla {talla}",
                categoria=categoria,
                genero_cliente=models.GeneroCliente.MUJER,
                talla=talla,
                precio=round(random.uniform(25.0, 150.0), 2),
                stock_actual=random.randint(0, 100),
                stock_minimo=5
            )
            productos.append(producto)
    
    # Productos para HOMBRE
    for categoria in CATEGORIAS_HOMBRE:
        for talla in TALLAS_ADULTOS:
            producto = models.Producto(
                nombre=f"{categoria.title()} Hombre Talla {talla}",
                categoria=categoria,
                genero_cliente=models.GeneroCliente.HOMBRE,
                talla=talla,
                precio=round(random.uniform(20.0, 120.0), 2),
                stock_actual=random.randint(0, 80),
                stock_minimo=5
            )
            productos.append(producto)
    
    # Productos para NIÑO/NIÑA (menos variedad)
    for categoria in CATEGORIAS_NIÑO:
        for talla in TALLAS_NIÑOS:
            producto = models.Producto(
                nombre=f"{categoria.title()} Niño Talla {talla}",
                categoria=categoria,
                genero_cliente=models.GeneroCliente.NIÑO,
                talla=talla,
                precio=round(random.uniform(15.0, 60.0), 2),
                stock_actual=random.randint(0, 50),
                stock_minimo=3
            )
            productos.append(producto)
    
    for categoria in CATEGORIAS_NIÑA:
        for talla in TALLAS_NIÑOS:
            producto = models.Producto(
                nombre=f"{categoria.title()} Niña Talla {talla}",
                categoria=categoria,
                genero_cliente=models.GeneroCliente.NIÑA,
                talla=talla,
                precio=round(random.uniform(15.0, 70.0), 2),
                stock_actual=random.randint(0, 50),
                stock_minimo=3
            )
            productos.append(producto)
    
    db.add_all(productos)
    db.commit()
    print(f"✅ {len(productos)} productos creados")
    return productos

def crear_ventas_ejemplo(db: Session, productos: list, sucursales: list):
    """Crear ventas de ejemplo para los últimos 3 meses"""
    ventas = []
    fecha_fin = datetime.now().date()
    fecha_inicio = fecha_fin - timedelta(days=90)
    
    # Crear 500 ventas de ejemplo
    for _ in range(500):
        producto = random.choice(productos)
        sucursal = random.choice(sucursales)
        fecha_venta = fecha_inicio + timedelta(days=random.randint(0, 90))
        cantidad = random.randint(1, 3)
        total = round(producto.precio * cantidad, 2)
        
        venta = models.Venta(
            producto_id=producto.id,
            fecha=fecha_venta,
            cantidad=cantidad,
            sucursal_id=sucursal.id,
            total=total
        )
        ventas.append(venta)
    
    db.add_all(ventas)
    db.commit()
    print(f"✅ {len(ventas)} ventas de ejemplo creadas")
    return ventas

def cargar_datos_ejemplo(db: Session):
    """Función principal para cargar todos los datos de ejemplo"""
    print("🔄 Cargando datos de ejemplo...")
    
    # Verificar si ya existen datos
    if db.query(models.Producto).count() > 0:
        print("⚠️ Ya existen datos en la base de datos. Saltando carga...")
        return
    
    sucursales = crear_sucursales_ejemplo(db)
    productos = crear_productos_ejemplo(db)
    ventas = crear_ventas_ejemplo(db, productos, sucursales)
    
    print("🎉 Datos de ejemplo cargados exitosamente!")
    return {"sucursales": len(sucursales), "productos": len(productos), "ventas": len(ventas)}

