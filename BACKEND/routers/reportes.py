from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime, timedelta

from database.connection import get_db
from database import models

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])

@router.get("/ventas-completo")
def reporte_ventas_completo(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Reporte completo de ventas con todos los detalles"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    query = db.query(models.Venta).join(models.Producto).join(models.Sucursal).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    )
    
    if sucursal_id:
        query = query.filter(models.Venta.sucursal_id == sucursal_id)
    
    ventas = query.all()
    
    # Resumen ejecutivo
    total_ventas = len(ventas)
    total_ingresos = sum(v.total for v in ventas)
    total_unidades = sum(v.cantidad for v in ventas)
    
    # Agrupaciones
    por_categoria = {}
    por_genero = {}
    por_sucursal = {}
    
    for venta in ventas:
        # Por categoría
        cat = venta.producto.categoria
        if cat not in por_categoria:
            por_categoria[cat] = {"ventas": 0, "ingresos": 0, "unidades": 0}
        por_categoria[cat]["ventas"] += 1
        por_categoria[cat]["ingresos"] += venta.total
        por_categoria[cat]["unidades"] += venta.cantidad
        
        # Por género
        gen = venta.producto.genero_cliente.value if hasattr(venta.producto.genero_cliente, 'value') else venta.producto.genero_cliente
        if gen not in por_genero:
            por_genero[gen] = {"ventas": 0, "ingresos": 0, "unidades": 0}
        por_genero[gen]["ventas"] += 1
        por_genero[gen]["ingresos"] += venta.total
        por_genero[gen]["unidades"] += venta.cantidad
        
        # Por sucursal
        suc = venta.sucursal.nombre
        if suc not in por_sucursal:
            por_sucursal[suc] = {"ventas": 0, "ingresos": 0, "unidades": 0}
        por_sucursal[suc]["ventas"] += 1
        por_sucursal[suc]["ingresos"] += venta.total
        por_sucursal[suc]["unidades"] += venta.cantidad
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "resumen_ejecutivo": {
            "total_ventas": total_ventas,
            "total_ingresos": f"${total_ingresos:,.2f}",
            "total_unidades": total_unidades,
            "ticket_promedio": f"${total_ingresos / total_ventas:,.2f}" if total_ventas > 0 else "$0.00"
        },
        "por_categoria": {
            cat: {
                "ventas": data["ventas"],
                "ingresos": f"${data['ingresos']:,.2f}",
                "unidades": data["unidades"],
                "participacion": f"{(data['ingresos'] / total_ingresos * 100):.1f}%"
            } for cat, data in por_categoria.items()
        },
        "por_genero": {
            gen: {
                "ventas": data["ventas"],
                "ingresos": f"${data['ingresos']:,.2f}",
                "unidades": data["unidades"],
                "participacion": f"{(data['ingresos'] / total_ingresos * 100):.1f}%"
            } for gen, data in por_genero.items()
        },
        "por_sucursal": {
            suc: {
                "ventas": data["ventas"],
                "ingresos": f"${data['ingresos']:,.2f}",
                "unidades": data["unidades"],
                "participacion": f"{(data['ingresos'] / total_ingresos * 100):.1f}%"
            } for suc, data in por_sucursal.items()
        }
    }

@router.get("/inventario-completo")
def reporte_inventario_completo(
    categoria: Optional[str] = None,
    genero: Optional[str] = None,
    con_stock_bajo: bool = False,
    db: Session = Depends(get_db)
):
    """Reporte completo del estado del inventario"""
    query = db.query(models.Producto)
    
    if categoria:
        query = query.filter(models.Producto.categoria == categoria.upper())
    
    if genero:
        query = query.filter(models.Producto.genero_cliente == genero)
    
    if con_stock_bajo:
        query = query.filter(models.Producto.stock_actual <= models.Producto.stock_minimo)
    
    productos = query.all()
    
    # Resumen
    total_productos = len(productos)
    valor_total = sum(p.stock_actual * p.precio for p in productos)
    stock_total = sum(p.stock_actual for p in productos)
    productos_criticos = sum(1 for p in productos if p.stock_actual <= p.stock_minimo)
    productos_sin_stock = sum(1 for p in productos if p.stock_actual == 0)
    
    # Por categoría
    por_categoria = {}
    for producto in productos:
        cat = producto.categoria
        if cat not in por_categoria:
            por_categoria[cat] = {
                "productos": 0,
                "stock_total": 0,
                "valor": 0,
                "criticos": 0
            }
        por_categoria[cat]["productos"] += 1
        por_categoria[cat]["stock_total"] += producto.stock_actual
        por_categoria[cat]["valor"] += producto.stock_actual * producto.precio
        if producto.stock_actual <= producto.stock_minimo:
            por_categoria[cat]["criticos"] += 1
    
    return {
        "resumen": {
            "total_productos": total_productos,
            "valor_total_inventario": f"${valor_total:,.2f}",
            "stock_total_unidades": stock_total,
            "stock_promedio": f"{stock_total / total_productos:.1f}" if total_productos > 0 else "0",
            "productos_criticos": productos_criticos,
            "productos_sin_stock": productos_sin_stock,
            "nivel_servicio": f"{((total_productos - productos_sin_stock) / total_productos * 100):.1f}%" if total_productos > 0 else "0%"
        },
        "por_categoria": {
            cat: {
                "productos": data["productos"],
                "stock_total": data["stock_total"],
                "valor": f"${data['valor']:,.2f}",
                "criticos": data["criticos"],
                "salud": "BUENA" if data["criticos"] == 0 else "REGULAR" if data["criticos"] < data["productos"] / 2 else "CRÍTICA"
            } for cat, data in por_categoria.items()
        },
        "productos_detalle": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "categoria": p.categoria,
                "genero": p.genero_cliente.value if hasattr(p.genero_cliente, 'value') else p.genero_cliente,
                "talla": p.talla,
                "precio": float(p.precio),
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "valor_stock": f"${p.stock_actual * p.precio:,.2f}",
                "estado": "CRÍTICO" if p.stock_actual == 0 else "BAJO" if p.stock_actual <= p.stock_minimo else "NORMAL"
            } for p in productos
        ]
    }

@router.get("/rendimiento-sucursales")
def reporte_rendimiento_sucursales(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Reporte de rendimiento comparativo por sucursales"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    sucursales = db.query(models.Sucursal).all()
    
    reporte_sucursales = []
    for sucursal in sucursales:
        ventas = db.query(models.Venta).filter(
            models.Venta.sucursal_id == sucursal.id,
            models.Venta.fecha >= fecha_inicio,
            models.Venta.fecha <= fecha_fin
        ).all()
        
        num_ventas = len(ventas)
        total_ingresos = sum(v.total for v in ventas)
        total_unidades = sum(v.cantidad for v in ventas)
        
        # Top 5 productos de esta sucursal
        top_productos = db.query(
            models.Producto.nombre,
            func.sum(models.Venta.cantidad).label('cantidad')
        ).join(models.Venta).filter(
            models.Venta.sucursal_id == sucursal.id,
            models.Venta.fecha >= fecha_inicio,
            models.Venta.fecha <= fecha_fin
        ).group_by(models.Producto.nombre).order_by(
            func.sum(models.Venta.cantidad).desc()
        ).limit(5).all()
        
        reporte_sucursales.append({
            "sucursal": sucursal.nombre,
            "ciudad": sucursal.ciudad,
            "metricas": {
                "num_ventas": num_ventas,
                "total_ingresos": f"${total_ingresos:,.2f}",
                "total_unidades": total_unidades,
                "ticket_promedio": f"${total_ingresos / num_ventas:,.2f}" if num_ventas > 0 else "$0.00",
                "unidades_por_venta": f"{total_unidades / num_ventas:.1f}" if num_ventas > 0 else "0"
            },
            "top_productos": [
                {
                    "producto": p.nombre,
                    "unidades_vendidas": int(p.cantidad)
                } for p in top_productos
            ]
        })
    
    # Ranking
    reporte_sucursales.sort(key=lambda x: float(x["metricas"]["total_ingresos"].replace("$", "").replace(",", "")), reverse=True)
    for i, suc in enumerate(reporte_sucursales, 1):
        suc["ranking"] = i
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "total_sucursales": len(sucursales),
        "sucursales": reporte_sucursales
    }

@router.get("/analisis-temporal")
def reporte_analisis_temporal(
    periodo: str = Query("diario", description="diario, semanal o mensual"),
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Reporte de análisis temporal de ventas"""
    if not fecha_inicio:
        fecha_inicio = str(datetime.now().date() - timedelta(days=30))
    if not fecha_fin:
        fecha_fin = str(datetime.now().date())
    
    ventas = db.query(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio,
        models.Venta.fecha <= fecha_fin
    ).all()
    
    # Agrupar por período
    agrupacion = {}
    
    for venta in ventas:
        if periodo == "diario":
            clave = str(venta.fecha)
        elif periodo == "semanal":
            # Agrupar por semana
            semana = venta.fecha.isocalendar()[1]
            clave = f"Semana {semana}"
        else:  # mensual
            clave = venta.fecha.strftime("%Y-%m")
        
        if clave not in agrupacion:
            agrupacion[clave] = {"ventas": 0, "ingresos": 0, "unidades": 0}
        agrupacion[clave]["ventas"] += 1
        agrupacion[clave]["ingresos"] += venta.total
        agrupacion[clave]["unidades"] += venta.cantidad
    
    # Ordenar por fecha
    datos_ordenados = sorted(agrupacion.items())
    
    return {
        "periodo": f"{fecha_inicio} a {fecha_fin}",
        "agrupacion": periodo,
        "datos": [
            {
                "periodo": clave,
                "ventas": data["ventas"],
                "ingresos": f"${data['ingresos']:,.2f}",
                "unidades": data["unidades"],
                "ticket_promedio": f"${data['ingresos'] / data['ventas']:,.2f}" if data['ventas'] > 0 else "$0.00"
            } for clave, data in datos_ordenados
        ]
    }

@router.get("/dashboard")
def dashboard_reportes(db: Session = Depends(get_db)):
    """Dashboard principal de reportes con resumen general"""
    
    # Período: último mes
    fecha_fin = datetime.now().date()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Ventas
    total_ventas = db.query(models.Venta).filter(
        models.Venta.fecha >= fecha_inicio
    ).count()
    
    total_ingresos = db.query(func.sum(models.Venta.total)).filter(
        models.Venta.fecha >= fecha_inicio
    ).scalar() or 0
    
    # Inventario
    total_productos = db.query(models.Producto).count()
    valor_inventario = db.query(
        func.sum(models.Producto.stock_actual * models.Producto.precio)
    ).scalar() or 0
    
    productos_criticos = db.query(models.Producto).filter(
        models.Producto.stock_actual <= models.Producto.stock_minimo
    ).count()
    
    # Sucursales
    total_sucursales = db.query(models.Sucursal).filter(
        models.Sucursal.activa == True
    ).count()
    
    return {
        "periodo": f"Últimos 30 días ({fecha_inicio} a {fecha_fin})",
        "resumen_general": {
            "ventas": {
                "total_transacciones": total_ventas,
                "total_ingresos": f"${total_ingresos:,.2f}",
                "ticket_promedio": f"${total_ingresos / total_ventas:,.2f}" if total_ventas > 0 else "$0.00"
            },
            "inventario": {
                "total_productos": total_productos,
                "valor_inventario": f"${valor_inventario:,.2f}",
                "productos_criticos": productos_criticos,
                "nivel_servicio": f"{((total_productos - productos_criticos) / total_productos * 100):.1f}%" if total_productos > 0 else "0%"
            },
            "operaciones": {
                "sucursales_activas": total_sucursales,
                "ventas_por_sucursal": f"{total_ventas / total_sucursales:.1f}" if total_sucursales > 0 else "0"
            }
        },
        "reportes_disponibles": [
            "/api/reportes/ventas-completo",
            "/api/reportes/inventario-completo",
            "/api/reportes/rendimiento-sucursales",
            "/api/reportes/analisis-temporal"
        ]
    }

