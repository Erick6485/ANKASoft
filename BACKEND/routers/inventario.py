from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta

from database.connection import get_db
from database import models

router = APIRouter(prefix="/api/inventario", tags=["Inventario"])

@router.get("/productos")
def obtener_productos(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    genero: Optional[str] = None,
    con_stock_bajo: bool = False,
    db: Session = Depends(get_db)
):
    """Obtener lista de productos con filtros"""
    query = db.query(models.Producto)
    
    if categoria:
        query = query.filter(models.Producto.categoria == categoria.upper())
    
    if genero:
        query = query.filter(models.Producto.genero_cliente == genero)
    
    if con_stock_bajo:
        query = query.filter(models.Producto.stock_actual <= models.Producto.stock_minimo)
    
    productos = query.offset(skip).limit(limit).all()
    
    return {
        "total": len(productos),
        "filtros": {
            "categoria": categoria,
            "genero": genero,
            "con_stock_bajo": con_stock_bajo
        },
        "productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "categoria": p.categoria,
                "genero_cliente": p.genero_cliente.value if hasattr(p.genero_cliente, 'value') else p.genero_cliente,
                "talla": p.talla,
                "precio": float(p.precio),
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo
            } for p in productos
        ]
    }

@router.get("/productos/{producto_id}")
def obtener_producto_detalle(producto_id: int, db: Session = Depends(get_db)):
    """Obtener detalle completo de un producto"""
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Obtener estadísticas de ventas del producto
    ventas_producto = db.query(models.Venta).filter(
        models.Venta.producto_id == producto_id
    ).all()
    
    total_vendido = sum(venta.cantidad for venta in ventas_producto)
    ultima_venta = max(venta.fecha for venta in ventas_producto) if ventas_producto else None
    
    return {
        "producto": {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "genero_cliente": producto.genero_cliente.value if hasattr(producto.genero_cliente, 'value') else producto.genero_cliente,
            "talla": producto.talla,
            "precio": float(producto.precio),
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo
        },
        "estadisticas": {
            "total_vendido": total_vendido,
            "ultima_venta": str(ultima_venta) if ultima_venta else None,
            "total_ventas": len(ventas_producto),
            "rotacion_mensual": calcular_rotacion_mensual(producto_id, db)
        }
    }

@router.put("/productos/{producto_id}/stock")
def actualizar_stock(
    producto_id: int,
    nuevo_stock: int,
    db: Session = Depends(get_db)
):
    """Actualizar stock de un producto"""
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.stock_actual = nuevo_stock
    db.commit()
    db.refresh(producto)
    
    return {
        "message": "Stock actualizado exitosamente",
        "producto": producto.nombre,
        "nuevo_stock": producto.stock_actual,
        "estado": "CRÍTICO" if producto.stock_actual <= producto.stock_minimo else "NORMAL"
    }

@router.post("/productos/{producto_id}/ajustar-stock")
def ajustar_stock(
    producto_id: int,
    ajuste: int,
    motivo: str,
    db: Session = Depends(get_db)
):
    """Ajustar stock (entradas/salidas de inventario)"""
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    stock_anterior = producto.stock_actual
    producto.stock_actual += ajuste
    
    if producto.stock_actual < 0:
        raise HTTPException(status_code=400, detail="Stock no puede ser negativo")
    
    # Registrar movimiento de inventario
    movimiento = models.MovimientoInventario(
        producto_id=producto_id,
        tipo="ENTRADA" if ajuste > 0 else "SALIDA",
        cantidad=abs(ajuste),
        stock_anterior=stock_anterior,
        stock_posterior=producto.stock_actual,
        motivo=motivo
    )
    
    db.add(movimiento)
    db.commit()
    db.refresh(producto)
    
    return {
        "message": "Stock ajustado exitosamente",
        "producto": producto.nombre,
        "ajuste": f"{'+' if ajuste > 0 else ''}{ajuste}",
        "stock_anterior": stock_anterior,
        "stock_actual": producto.stock_actual,
        "motivo": motivo
    }

@router.get("/alertas")
def obtener_alertas_inventario(db: Session = Depends(get_db)):
    """Obtener alertas de inventario categorizadas"""
    productos = db.query(models.Producto).all()
    
    alertas = {
        "stock_critico": [],
        "stock_bajo": [],
        "sin_movimiento_30_dias": [],
        "alta_rotacion": []
    }
    
    for producto in productos:
        if producto.stock_actual == 0:
            alertas["stock_critico"].append({
                "producto": producto.nombre,
                "categoria": producto.categoria,
                "stock_actual": producto.stock_actual,
                "stock_minimo": producto.stock_minimo,
                "prioridad": "ALTA"
            })
        elif producto.stock_actual <= producto.stock_minimo:
            alertas["stock_bajo"].append({
                "producto": producto.nombre,
                "categoria": producto.categoria,
                "stock_actual": producto.stock_actual,
                "prioridad": "MEDIA"
            })
    
    return {
        "total_alertas": len(alertas["stock_critico"]) + len(alertas["stock_bajo"]),
        "alertas": alertas
    }

@router.get("/reportes/rotacion")
def reporte_rotacion_inventario(
    periodo_dias: int = Query(30, description="Período en días para calcular rotación"),
    db: Session = Depends(get_db)
):
    """Reporte de rotación de inventario"""
    fecha_limite = datetime.now().date() - timedelta(days=periodo_dias)
    
    # Productos con mayor rotación
    productos_rotacion = db.query(
        models.Producto.id,
        models.Producto.nombre,
        models.Producto.categoria,
        models.Producto.stock_actual,
        func.sum(models.Venta.cantidad).label("ventas_periodo")
    ).join(models.Venta).filter(
        models.Venta.fecha >= fecha_limite
    ).group_by(models.Producto.id).order_by(
        func.sum(models.Venta.cantidad).desc()
    ).limit(20).all()
    
    # Productos sin movimiento
    productos_sin_movimiento = db.query(models.Producto).filter(
        ~models.Producto.id.in_(
            db.query(models.Venta.producto_id).filter(
                models.Venta.fecha >= fecha_limite
            )
        )
    ).limit(20).all()
    
    return {
        "periodo": f"Últimos {periodo_dias} días",
        "productos_alta_rotacion": [
            {
                "producto": p.nombre,
                "categoria": p.categoria,
                "stock_actual": p.stock_actual,
                "ventas_periodo": int(p.ventas_periodo),
                "rotacion": f"{(p.ventas_periodo / p.stock_actual * 100) if p.stock_actual > 0 else 0:.1f}%"
            } for p in productos_rotacion
        ],
        "productos_sin_movimiento": [
            {
                "producto": p.nombre,
                "categoria": p.categoria,
                "stock_actual": p.stock_actual,
                "ultima_venta": "Sin ventas en el período"
            } for p in productos_sin_movimiento
        ]
    }

@router.get("/dashboard-inventario")
def dashboard_inventario(db: Session = Depends(get_db)):
    """Dashboard específico para gestión de inventario"""
    total_productos = db.query(models.Producto).count()
    productos_stock_bajo = db.query(models.Producto).filter(
        models.Producto.stock_actual <= models.Producto.stock_minimo
    ).count()
    
    # Valor total del inventario
    valor_inventario = db.query(
        func.sum(models.Producto.stock_actual * models.Producto.precio)
    ).scalar() or 0
    
    # Productos próximos a agotarse
    productos_proximos_agotar = db.query(models.Producto).filter(
        models.Producto.stock_actual < 5
    ).count()
    
    return {
        "resumen": {
            "total_productos": total_productos,
            "productos_stock_bajo": productos_stock_bajo,
            "productos_proximos_agotar": productos_proximos_agotar,
            "valor_total_inventario": f"${valor_inventario:,.2f}",
            "nivel_servicio": f"{(1 - productos_stock_bajo / total_productos) * 100:.1f}%" if total_productos > 0 else "100%"
        },
        "metricas_clave": {
            "indice_rotacion": calcular_indice_rotacion_promedio(db),
            "cobertura_inventario": calcular_cobertura_inventario(db),
            "eficiencia_espacio": calcular_eficiencia_espacio(db)
        }
    }

# Funciones auxiliares
def calcular_rotacion_mensual(producto_id: int, db: Session):
    """Calcular rotación mensual de un producto"""
    ventas_30_dias = db.query(models.Venta).filter(
        models.Venta.producto_id == producto_id,
        models.Venta.fecha >= datetime.now().date() - timedelta(days=30)
    ).count()
    
    return ventas_30_dias

def calcular_indice_rotacion_promedio(db: Session):
    """Calcular índice de rotación promedio del inventario"""
    total_ventas_30_dias = db.query(models.Venta).filter(
        models.Venta.fecha >= datetime.now().date() - timedelta(days=30)
    ).count()
    
    total_productos = db.query(models.Producto).count()
    
    return round(total_ventas_30_dias / total_productos, 2) if total_productos > 0 else 0

def calcular_cobertura_inventario(db: Session):
    """Calcular cobertura promedio del inventario en días"""
    productos_con_stock = db.query(models.Producto).filter(
        models.Producto.stock_actual > 0
    ).count()
    
    total_productos = db.query(models.Producto).count()
    
    return round((productos_con_stock / total_productos) * 100, 1) if total_productos > 0 else 0

def calcular_eficiencia_espacio(db: Session):
    """Calcular eficiencia de uso de espacio en inventario"""
    productos_optimos = db.query(models.Producto).filter(
        models.Producto.stock_actual > models.Producto.stock_minimo,
        models.Producto.stock_actual <= 50
    ).count()
    
    total_productos = db.query(models.Producto).count()
    
    return round((productos_optimos / total_productos) * 100, 1) if total_productos > 0 else 0

