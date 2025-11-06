from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime, timedelta, date

from database.connection import get_db
from database import models

router = APIRouter(prefix="/api/ventas", tags=["Ventas"])

@router.get("/dashboard-ventas")
def dashboard_ventas(db: Session = Depends(get_db)):
    """Dashboard completo de ventas"""
    hoy = datetime.now().date()
    mes_actual = hoy.month
    
    # Ventas de hoy
    ventas_hoy = db.query(models.Venta).filter(models.Venta.fecha == hoy).count()
    ingresos_hoy = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha == hoy
    ).scalar() or 0
    
    # Ventas del mes
    ventas_mes = db.query(models.Venta).filter(
        extract('month', models.Venta.fecha) == mes_actual
    ).count()
    ingresos_mes = db.query(func.sum(models.Venta.total)).filter(
        extract('month', models.Venta.fecha) == mes_actual
    ).scalar() or 0
    
    # Tendencia (últimos 7 días)
    hace_7_dias = hoy - timedelta(days=7)
    ventas_por_dia = []
    for i in range(7):
        dia = hace_7_dias + timedelta(days=i)
        ventas_dia = db.query(func.sum(models.Venta.total)).filter(
            models.Venta.fecha == dia
        ).scalar() or 0
        ventas_por_dia.append({
            "fecha": str(dia),
            "total": float(ventas_dia)
        })
    
    return {
        "hoy": {
            "ventas": ventas_hoy,
            "ingresos": f"${ingresos_hoy:,.2f}",
            "ticket_promedio": f"${ingresos_hoy / ventas_hoy:,.2f}" if ventas_hoy > 0 else "$0.00"
        },
        "mes_actual": {
            "ventas": ventas_mes,
            "ingresos": f"${ingresos_mes:,.2f}",
            "ticket_promedio": f"${ingresos_mes / ventas_mes:,.2f}" if ventas_mes > 0 else "$0.00"
        },
        "tendencia_7_dias": ventas_por_dia
    }

@router.get("/")
def obtener_ventas(
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    sucursal_id: Optional[int] = None,
    producto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de ventas con filtros"""
    query = db.query(models.Venta).join(models.Producto).join(models.Sucursal)
    
    if fecha_inicio:
        query = query.filter(models.Venta.fecha >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(models.Venta.fecha <= fecha_fin)
    
    if sucursal_id:
        query = query.filter(models.Venta.sucursal_id == sucursal_id)
    
    if producto_id:
        query = query.filter(models.Venta.producto_id == producto_id)
    
    ventas = query.order_by(models.Venta.fecha.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": len(ventas),
        "filtros": {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "sucursal_id": sucursal_id,
            "producto_id": producto_id
        },
        "ventas": [
            {
                "id": v.id,
                "fecha": str(v.fecha),
                "producto": v.producto.nombre,
                "categoria": v.producto.categoria,
                "cantidad": v.cantidad,
                "precio_unitario": float(v.producto.precio),
                "total": float(v.total),
                "sucursal": v.sucursal.nombre
            } for v in ventas
        ]
    }

@router.get("/resumen/diario")
def resumen_ventas_diario(
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Resumen de ventas del día"""
    if not fecha:
        fecha = str(datetime.now().date())
    
    ventas_dia = db.query(models.Venta).filter(
        models.Venta.fecha == fecha
    ).all()
    
    total_ventas = len(ventas_dia)
    total_unidades = sum(v.cantidad for v in ventas_dia)
    total_ingresos = sum(v.total for v in ventas_dia)
    
    # Ventas por sucursal
    ventas_por_sucursal = db.query(
        models.Sucursal.nombre,
        func.count(models.Venta.id).label("num_ventas"),
        func.sum(models.Venta.total).label("total")
    ).join(models.Venta).filter(
        models.Venta.fecha == fecha
    ).group_by(models.Sucursal.nombre).all()
    
    return {
        "fecha": fecha,
        "resumen": {
            "total_ventas": total_ventas,
            "total_unidades": total_unidades,
            "total_ingresos": f"${total_ingresos:,.2f}",
            "ticket_promedio": f"${total_ingresos / total_ventas:,.2f}" if total_ventas > 0 else "$0.00"
        },
        "por_sucursal": [
            {
                "sucursal": v.nombre,
                "num_ventas": v.num_ventas,
                "total": f"${float(v.total):,.2f}"
            } for v in ventas_por_sucursal
        ]
    }

@router.get("/resumen/mensual")
def resumen_ventas_mensual(
    mes: Optional[int] = Query(None, description="Mes (1-12)"),
    anio: Optional[int] = Query(None, description="Año"),
    db: Session = Depends(get_db)
):
    """Resumen de ventas del mes"""
    if not mes:
        mes = datetime.now().month
    if not anio:
        anio = datetime.now().year
    
    ventas_mes = db.query(models.Venta).filter(
        extract('month', models.Venta.fecha) == mes,
        extract('year', models.Venta.fecha) == anio
    ).all()
    
    total_ventas = len(ventas_mes)
    total_unidades = sum(v.cantidad for v in ventas_mes)
    total_ingresos = sum(v.total for v in ventas_mes)
    
    # Top productos del mes
    top_productos = db.query(
        models.Producto.nombre,
        func.sum(models.Venta.cantidad).label("cantidad"),
        func.sum(models.Venta.total).label("total")
    ).join(models.Venta).filter(
        extract('month', models.Venta.fecha) == mes,
        extract('year', models.Venta.fecha) == anio
    ).group_by(models.Producto.nombre).order_by(
        func.sum(models.Venta.cantidad).desc()
    ).limit(10).all()
    
    return {
        "periodo": f"{mes:02d}/{anio}",
        "resumen": {
            "total_ventas": total_ventas,
            "total_unidades": total_unidades,
            "total_ingresos": f"${total_ingresos:,.2f}",
            "ticket_promedio": f"${total_ingresos / total_ventas:,.2f}" if total_ventas > 0 else "$0.00"
        },
        "top_productos": [
            {
                "producto": p.nombre,
                "unidades_vendidas": int(p.cantidad),
                "ingresos": f"${float(p.total):,.2f}"
            } for p in top_productos
        ]
    }

@router.get("/reportes/por-vendedor")
def reporte_ventas_por_vendedor(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Reporte de ventas por vendedor/sucursal"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    ventas_por_sucursal = db.query(
        models.Sucursal.nombre,
        models.Sucursal.ciudad,
        func.count(models.Venta.id).label("num_ventas"),
        func.sum(models.Venta.cantidad).label("unidades"),
        func.sum(models.Venta.total).label("ingresos")
    ).join(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).group_by(models.Sucursal.id).order_by(
        func.sum(models.Venta.total).desc()
    ).all()
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "sucursales": [
            {
                "sucursal": s.nombre,
                "ciudad": s.ciudad,
                "num_ventas": s.num_ventas,
                "unidades_vendidas": int(s.unidades) if s.unidades else 0,
                "ingresos_totales": f"${float(s.ingresos):,.2f}" if s.ingresos else "$0.00",
                "ticket_promedio": f"${float(s.ingresos) / s.num_ventas:,.2f}" if s.num_ventas > 0 else "$0.00"
            } for s in ventas_por_sucursal
        ]
    }

