from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from database.connection import get_db
from database import models
from services.analytics_service import AnalyticsService
from services.association_rules import AssociationRulesService
from database.schemas import KPIFilters
from utils.data_loader import cargar_datos_ejemplo
from utils.security import verify_api_key

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/productos-mas-vendidos", dependencies=[Depends(verify_api_key)])
def obtener_productos_mas_vendidos(
    mes: Optional[int] = Query(None, description="Mes (1-12)"),
    categoria: Optional[str] = Query(None, description="Categoría de producto"),
    limite: int = Query(10, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Endpoint para obtener los productos más vendidos"""
    try:
        resultados = AnalyticsService.get_productos_mas_vendidos(
            db=db, 
            mes=mes, 
            categoria=categoria, 
            limite=limite
        )
        
        # Convertir resultados a formato JSON
        productos = []
        for r in resultados:
            productos.append({
                "producto_id": r.producto_id,
                "nombre": r.nombre,
                "categoria": r.categoria,
                "genero_cliente": r.genero_cliente.value if hasattr(r.genero_cliente, 'value') else str(r.genero_cliente),
                "talla": r.talla,
                "total_vendido": float(r.total_vendido) if r.total_vendido else 0,
                "ingreso_total": float(r.ingreso_total) if r.ingreso_total else 0
            })
            
        return {
            "filtros": {"mes": mes, "categoria": categoria},
            "total_resultados": len(productos),
            "productos": productos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

@router.get("/rotacion-tallas", dependencies=[Depends(verify_api_key)])
def obtener_rotacion_tallas(
    genero: Optional[str] = Query(None, description="Género del cliente (mujer, hombre, niño, niña)"),
    db: Session = Depends(get_db)
):
    """Endpoint para análisis de rotación por tallas"""
    try:
        resultados = AnalyticsService.get_rotacion_tallas(db=db, genero=genero)
        
        rotacion = []
        for r in resultados:
            rotacion.append({
                "talla": r.talla,
                "genero_cliente": r.genero_cliente.value if hasattr(r.genero_cliente, 'value') else str(r.genero_cliente),
                "total_vendido": float(r.total_vendido) if r.total_vendido else 0,
                "num_ventas": r.num_ventas
            })
            
        return {
            "filtros": {"genero": genero},
            "rotacion_tallas": rotacion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

@router.get("/alertas-stock", dependencies=[Depends(verify_api_key)])
def obtener_alertas_stock(db: Session = Depends(get_db)):
    """Endpoint para alertas de stock crítico"""
    try:
        alertas = AnalyticsService.get_stock_alerts(db=db)
        
        productos_alerta = []
        for producto in alertas:
            productos_alerta.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "genero_cliente": producto.genero_cliente.value if hasattr(producto.genero_cliente, 'value') else str(producto.genero_cliente),
                "talla": producto.talla,
                "stock_actual": producto.stock_actual,
                "stock_minimo": producto.stock_minimo,
                "estado": "CRÍTICO" if producto.stock_actual == 0 else "BAJO"
            })
            
        return {
            "total_alertas": len(productos_alerta),
            "alertas": productos_alerta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alertas: {str(e)}")

@router.get("/comparativo-generos", dependencies=[Depends(verify_api_key)])
def obtener_comparativo_generos(
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Endpoint para comparativo de ventas por género"""
    try:
        resultados = AnalyticsService.get_comparativo_generos(
            db=db, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin
        )
        
        comparativo = []
        for r in resultados:
            comparativo.append({
                "genero_cliente": r.genero_cliente.value if hasattr(r.genero_cliente, 'value') else str(r.genero_cliente),
                "total_unidades": float(r.total_unidades) if r.total_unidades else 0,
                "total_ingresos": float(r.total_ingresos) if r.total_ingresos else 0,
                "total_ventas": r.total_ventas
            })
            
        return {
            "filtros": {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
            "comparativo_generos": comparativo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comparativo: {str(e)}")

@router.post("/cargar-datos-ejemplo")
def cargar_datos_de_ejemplo(db: Session = Depends(get_db)):
    """Endpoint para cargar datos de ejemplo en la base de datos (solo desarrollo)"""
    try:
        resultado = cargar_datos_ejemplo(db)
        return {
            "message": "Datos de ejemplo cargados exitosamente",
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al cargar datos de ejemplo: {str(e)}"
        )

@router.get("/recomendaciones-inteligentes", dependencies=[Depends(verify_api_key)])
def obtener_recomendaciones_inteligentes(db: Session = Depends(get_db)):
    """Endpoint innovador: Recomendaciones automáticas para la empresa"""
    try:
        recomendaciones = AnalyticsService.get_recomendaciones_inteligentes(db)
        
        # Estadísticas de recomendaciones
        stats = {
            "total_recomendaciones": len(recomendaciones),
            "por_tipo": {},
            "por_prioridad": {"ALTA": 0, "MEDIA": 0, "BAJA": 0}
        }
        
        for rec in recomendaciones:
            stats["por_tipo"][rec["tipo"]] = stats["por_tipo"].get(rec["tipo"], 0) + 1
            stats["por_prioridad"][rec["prioridad"]] += 1
            
        return {
            "recomendaciones": recomendaciones,
            "estadisticas": stats,
            "message": f"Se generaron {len(recomendaciones)} recomendaciones inteligentes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

@router.get("/prediccion-ventas", dependencies=[Depends(verify_api_key)])
def obtener_prediccion_ventas(
    categoria: Optional[str] = Query(None, description="Categoría específica para predicción"),
    db: Session = Depends(get_db)
):
    """Endpoint innovador: Predicciones simples de ventas"""
    try:
        predicciones = AnalyticsService.get_prediccion_ventas_simple(db, categoria)
        
        return {
            "filtros": {"categoria": categoria},
            "predicciones": predicciones,
            "metodologia": "Promedio móvil de últimos 3 meses con factor de crecimiento del 10%",
            "total_categorias": len(predicciones)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar predicciones: {str(e)}")

@router.get("/dashboard-resumen", dependencies=[Depends(verify_api_key)])
def obtener_dashboard_resumen(
    mes: Optional[int] = Query(None, description="Mes para el resumen (1-12)"),
    db: Session = Depends(get_db)
):
    """Endpoint TODO-EN-UNO: Resumen completo para dashboard"""
    try:
        # Múltiples KPIs en una sola llamada
        productos_top = AnalyticsService.get_productos_mas_vendidos(db, mes=mes, limite=5)
        alertas_stock = AnalyticsService.get_stock_alerts(db)
        comparativo_generos = AnalyticsService.get_comparativo_generos(db)
        recomendaciones = AnalyticsService.get_recomendaciones_inteligentes(db)
        
        # Calcular métricas resumen
        total_productos = db.query(models.Producto).count()
        total_ventas_mes = db.query(func.sum(models.Venta.cantidad)).filter(
            extract('month', models.Venta.fecha) == mes
        ).scalar() or 0
        
        return {
            "resumen_general": {
                "total_productos": total_productos,
                "total_ventas_mes": float(total_ventas_mes),
                "alertas_activas": len(alertas_stock),
                "recomendaciones": len(recomendaciones)
            },
            "productos_destacados": [
                {
                    "nombre": p.nombre,
                    "categoria": p.categoria,
                    "total_vendido": float(p.total_vendido),
                    "ingreso_total": float(p.ingreso_total)
                } for p in productos_top
            ],
            "comparativo_generos": [
                {
                    "genero": g.genero_cliente.value if hasattr(g.genero_cliente, 'value') else str(g.genero_cliente),
                    "total_unidades": float(g.total_unidades),
                    "total_ingresos": float(g.total_ingresos)
                } for g in comparativo_generos
            ],
            "alertas_prioritarias": [
                {
                    "producto": a.nombre,
                    "stock_actual": a.stock_actual,
                    "stock_minimo": a.stock_minimo,
                    "estado": "CRÍTICO" if a.stock_actual == 0 else "BAJO"
                } for a in alertas_stock[:5]  # Solo las primeras 5
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar dashboard: {str(e)}")

@router.get("/reglas-asociacion", dependencies=[Depends(verify_api_key)])
def obtener_reglas_asociacion(
    confianza_minima: float = Query(0.5, description="Confianza mínima (0.0 - 1.0)"),
    soporte_minimo: float = Query(0.1, description="Soporte mínimo (0.0 - 1.0)"),
    db: Session = Depends(get_db)
):
    """Endpoint innovador: Descubre patrones de compra 'Los que compran X también compran Y'"""
    try:
        reglas = AssociationRulesService.encontrar_reglas_asociacion(
            db, confianza_minima, soporte_minimo
        )
        
        return {
            "parametros": {
                "confianza_minima": f"{confianza_minima * 100}%",
                "soporte_minimo": f"{soporte_minimo * 100}%"
            },
            "total_reglas": len(reglas),
            "reglas": reglas,
            "interpretacion": "Ejemplo: {Camiseta} → {Jeans} significa que los que compran Camisetas también compran Jeans"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular reglas: {str(e)}")

@router.get("/recomendaciones-cruzadas/{categoria}", dependencies=[Depends(verify_api_key)])
def obtener_recomendaciones_cruzadas(
    categoria: str,
    db: Session = Depends(get_db)
):
    """Endpoint para recomendaciones de productos relacionados"""
    try:
        recomendaciones = AssociationRulesService.get_recomendaciones_cruzadas(db, categoria.upper())
        
        return {
            "categoria_consulta": categoria,
            "recomendaciones": recomendaciones,
            "uso_practico": "Útil para: cross-selling, ubicación en tienda, promociones combinadas"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

