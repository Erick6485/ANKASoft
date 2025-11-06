from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime, timedelta

from database.connection import get_db
from database import models

router = APIRouter(prefix="/api/kpis", tags=["KPIs"])

@router.get("/dashboard")
def dashboard_kpis(db: Session = Depends(get_db)):
    """Dashboard completo de KPIs principales"""
    
    # Período: último mes
    fecha_fin = datetime.now().date()
    fecha_inicio = fecha_fin - timedelta(days=30)
    mes_anterior_inicio = fecha_inicio - timedelta(days=30)
    
    # KPI 1: Ventas totales
    ventas_periodo = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    ventas_periodo_anterior = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha >= mes_anterior_inicio,
        models.Venta.fecha < fecha_inicio
    ).scalar() or 0
    
    variacion_ventas = calcular_variacion(ventas_periodo, ventas_periodo_anterior)
    
    # KPI 2: Número de transacciones
    num_transacciones = db.query(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio
    ).count()
    
    num_transacciones_anterior = db.query(models.Venta).filter(
        models.Venta.fecha >= mes_anterior_inicio,
        models.Venta.fecha < fecha_inicio
    ).count()
    
    variacion_transacciones = calcular_variacion(num_transacciones, num_transacciones_anterior)
    
    # KPI 3: Ticket promedio
    ticket_promedio = ventas_periodo / num_transacciones if num_transacciones > 0 else 0
    ticket_promedio_anterior = ventas_periodo_anterior / num_transacciones_anterior if num_transacciones_anterior > 0 else 0
    variacion_ticket = calcular_variacion(ticket_promedio, ticket_promedio_anterior)
    
    # KPI 4: Tasa de conversión (productos con ventas vs total productos)
    productos_vendidos = db.query(func.count(func.distinct(models.Venta.producto_id))).filter(
        models.Venta.fecha >= fecha_inicio
    ).scalar() or 0
    
    total_productos = db.query(models.Producto).count()
    tasa_conversion = (productos_vendidos / total_productos * 100) if total_productos > 0 else 0
    
    # KPI 5: Valor promedio por cliente (asumiendo 1 cliente por transacción)
    valor_promedio_cliente = ventas_periodo / num_transacciones if num_transacciones > 0 else 0
    
    # KPI 6: Rotación de inventario
    inventario_promedio = db.query(func.avg(models.Producto.stock_actual)).scalar() or 0
    unidades_vendidas = db.query(func.sum(models.Venta.cantidad)).filter(
        models.Venta.fecha >= fecha_inicio
    ).scalar() or 0
    
    rotacion_inventario = (unidades_vendidas / inventario_promedio) if inventario_promedio > 0 else 0
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "kpis_principales": {
            "ventas_totales": {
                "valor": f"${ventas_periodo:,.2f}",
                "variacion": f"{variacion_ventas:+.1f}%",
                "tendencia": "positiva" if variacion_ventas > 0 else "negativa"
            },
            "num_transacciones": {
                "valor": num_transacciones,
                "variacion": f"{variacion_transacciones:+.1f}%",
                "tendencia": "positiva" if variacion_transacciones > 0 else "negativa"
            },
            "ticket_promedio": {
                "valor": f"${ticket_promedio:,.2f}",
                "variacion": f"{variacion_ticket:+.1f}%",
                "tendencia": "positiva" if variacion_ticket > 0 else "negativa"
            },
            "tasa_conversion": {
                "valor": f"{tasa_conversion:.1f}%",
                "descripcion": f"{productos_vendidos} de {total_productos} productos con ventas"
            },
            "valor_promedio_cliente": {
                "valor": f"${valor_promedio_cliente:,.2f}",
                "descripcion": "Gasto promedio por transacción"
            },
            "rotacion_inventario": {
                "valor": f"{rotacion_inventario:.2f}",
                "descripcion": "Veces que rota el inventario en el período"
            }
        }
    }

@router.get("/ventas")
def kpis_ventas(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """KPIs específicos de ventas"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    # Total de ventas
    total_ventas = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    # Número de ventas
    num_ventas = db.query(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).count()
    
    # Unidades vendidas
    unidades_vendidas = db.query(func.sum(models.Venta.cantidad)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    # Venta máxima
    venta_maxima = db.query(func.max(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    # Venta mínima
    venta_minima = db.query(func.min(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    # Ventas por día de la semana
    ventas_por_dia = db.query(
        extract('dow', models.Venta.fecha).label('dia_semana'),
        func.count(models.Venta.id).label('num_ventas'),
        func.sum(models.Venta.total).label('total')
    ).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).group_by('dia_semana').all()
    
    dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "resumen": {
            "total_ventas": f"${total_ventas:,.2f}",
            "num_ventas": num_ventas,
            "unidades_vendidas": int(unidades_vendidas),
            "ticket_promedio": f"${total_ventas / num_ventas:,.2f}" if num_ventas > 0 else "$0.00",
            "venta_maxima": f"${venta_maxima:,.2f}",
            "venta_minima": f"${venta_minima:,.2f}"
        },
        "ventas_por_dia_semana": [
            {
                "dia": dias_semana[int(v.dia_semana)],
                "num_ventas": v.num_ventas,
                "total": f"${float(v.total):,.2f}",
                "promedio": f"${float(v.total) / v.num_ventas:,.2f}"
            } for v in ventas_por_dia
        ]
    }

@router.get("/inventario")
def kpis_inventario(db: Session = Depends(get_db)):
    """KPIs específicos de inventario"""
    
    # Total productos
    total_productos = db.query(models.Producto).count()
    
    # Valor total inventario
    valor_inventario = db.query(
        func.sum(models.Producto.stock_actual * models.Producto.precio)
    ).scalar() or 0
    
    # Stock promedio
    stock_promedio = db.query(func.avg(models.Producto.stock_actual)).scalar() or 0
    
    # Productos con stock bajo
    productos_stock_bajo = db.query(models.Producto).filter(
        models.Producto.stock_actual <= models.Producto.stock_minimo
    ).count()
    
    # Productos sin stock
    productos_sin_stock = db.query(models.Producto).filter(
        models.Producto.stock_actual == 0
    ).count()
    
    # Cobertura de inventario
    cobertura = ((total_productos - productos_stock_bajo) / total_productos * 100) if total_productos > 0 else 0
    
    # Productos con sobrestock (más de 50 unidades)
    productos_sobrestock = db.query(models.Producto).filter(
        models.Producto.stock_actual > 50
    ).count()
    
    return {
        "resumen": {
            "total_productos": total_productos,
            "valor_inventario": f"${valor_inventario:,.2f}",
            "stock_promedio": f"{stock_promedio:.1f} unidades",
            "productos_stock_bajo": productos_stock_bajo,
            "productos_sin_stock": productos_sin_stock,
            "cobertura_inventario": f"{cobertura:.1f}%",
            "productos_sobrestock": productos_sobrestock
        },
        "metricas_salud": {
            "nivel_servicio": f"{((total_productos - productos_sin_stock) / total_productos * 100):.1f}%",
            "tasa_desabastecimiento": f"{(productos_stock_bajo / total_productos * 100):.1f}%",
            "eficiencia_inventario": f"{((total_productos - productos_sobrestock - productos_stock_bajo) / total_productos * 100):.1f}%"
        }
    }

@router.get("/rentabilidad")
def kpis_rentabilidad(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """KPIs de rentabilidad y márgenes"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    # Ingresos totales
    ingresos_totales = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).scalar() or 0
    
    # Categorías más rentables
    rentabilidad_categoria = db.query(
        models.Producto.categoria,
        func.sum(models.Venta.total).label('ingresos'),
        func.sum(models.Venta.cantidad).label('unidades')
    ).join(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).group_by(models.Producto.categoria).order_by(
        func.sum(models.Venta.total).desc()
    ).limit(10).all()
    
    # Productos más rentables
    productos_rentables = db.query(
        models.Producto.nombre,
        models.Producto.categoria,
        func.sum(models.Venta.total).label('ingresos'),
        func.sum(models.Venta.cantidad).label('unidades')
    ).join(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).group_by(models.Producto.id).order_by(
        func.sum(models.Venta.total).desc()
    ).limit(10).all()
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "resumen": {
            "ingresos_totales": f"${ingresos_totales:,.2f}",
            "ingresos_promedio_dia": f"${ingresos_totales / 30:,.2f}"
        },
        "por_categoria": [
            {
                "categoria": c.categoria,
                "ingresos": f"${float(c.ingresos):,.2f}",
                "unidades": int(c.unidades),
                "participacion": f"{(float(c.ingresos) / ingresos_totales * 100):.1f}%"
            } for c in rentabilidad_categoria
        ],
        "top_productos": [
            {
                "producto": p.nombre,
                "categoria": p.categoria,
                "ingresos": f"${float(p.ingresos):,.2f}",
                "unidades": int(p.unidades)
            } for p in productos_rentables
        ]
    }

# Función auxiliar
def calcular_variacion(valor_actual, valor_anterior):
    """Calcular variación porcentual"""
    if valor_anterior == 0:
        return 100.0 if valor_actual > 0 else 0.0
    return ((valor_actual - valor_anterior) / valor_anterior) * 100

