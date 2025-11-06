from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case, and_
from datetime import datetime, timedelta
from database import models
from typing import List, Dict, Any

class AnalyticsService:
    
    @staticmethod
    def get_productos_mas_vendidos(db: Session, mes: int = None, categoria: str = None, limite: int = 10):
        """Top productos más vendidos con filtros opcionales"""
        query = db.query(
            models.Venta.producto_id,
            models.Producto.nombre,
            models.Producto.categoria,
            models.Producto.genero_cliente,
            models.Producto.talla,
            func.sum(models.Venta.cantidad).label("total_vendido"),
            func.sum(models.Venta.total).label("ingreso_total")
        ).join(models.Producto)
        
        if mes:
            query = query.filter(extract('month', models.Venta.fecha) == mes)
        
        if categoria:
            query = query.filter(models.Producto.categoria == categoria)
            
        return query.group_by(
            models.Venta.producto_id,
            models.Producto.nombre,
            models.Producto.categoria,
            models.Producto.genero_cliente,
            models.Producto.talla
        ).order_by(func.sum(models.Venta.cantidad).desc()).limit(limite).all()
    
    @staticmethod
    def get_rotacion_tallas(db: Session, genero: str = None):
        """Análisis de rotación por tallas"""
        query = db.query(
            models.Producto.talla,
            models.Producto.genero_cliente,
            func.sum(models.Venta.cantidad).label("total_vendido"),
            func.count(models.Venta.id).label("num_ventas")
        ).join(models.Venta)
        
        if genero:
            # Convertir string a Enum
            try:
                genero_enum = models.GeneroCliente[genero.upper()]
                query = query.filter(models.Producto.genero_cliente == genero_enum)
            except KeyError:
                pass  # Si el género no es válido, ignorar el filtro
            
        return query.group_by(
            models.Producto.talla,
            models.Producto.genero_cliente
        ).order_by(func.sum(models.Venta.cantidad).desc()).all()
    
    @staticmethod
    def get_stock_alerts(db: Session, stock_minimo: int = 5):
        """Alertas de stock crítico"""
        return db.query(models.Producto).filter(
            models.Producto.stock_actual <= models.Producto.stock_minimo
        ).all()
    
    @staticmethod
    def get_comparativo_generos(db: Session, fecha_inicio: str = None, fecha_fin: str = None):
        """Comparativo de ventas por género"""
        query = db.query(
            models.Producto.genero_cliente,
            func.sum(models.Venta.cantidad).label("total_unidades"),
            func.sum(models.Venta.total).label("total_ingresos"),
            func.count(models.Venta.id).label("total_ventas")
        ).join(models.Venta)
        
        if fecha_inicio:
            query = query.filter(models.Venta.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(models.Venta.fecha <= fecha_fin)
            
        return query.group_by(models.Producto.genero_cliente).all()
    
    @staticmethod
    def get_recomendaciones_inteligentes(db: Session):
        """Recomendaciones automáticas basadas en análisis de datos"""
        recomendaciones = []
        
        # 1. Productos con baja rotación (sugerir descuentos)
        productos_baja_rotacion = db.query(
            models.Producto.id,
            models.Producto.nombre,
            models.Producto.categoria,
            models.Producto.stock_actual,
            func.coalesce(func.sum(models.Venta.cantidad), 0).label("ventas_30_dias")
        ).outerjoin(models.Venta, and_(
            models.Venta.producto_id == models.Producto.id,
            models.Venta.fecha >= datetime.now().date() - timedelta(days=30)
        )).group_by(models.Producto.id).having(
            func.coalesce(func.sum(models.Venta.cantidad), 0) < 5
        ).all()
        
        for producto in productos_baja_rotacion:
            if producto.stock_actual > 10:
                recomendaciones.append({
                    "tipo": "DESCUENTO_RECOMMENDADO",
                    "producto_id": producto.id,
                    "producto_nombre": producto.nombre,
                    "categoria": producto.categoria,
                    "motivo": f"Baja rotación ({producto.ventas_30_dias} ventas en 30 días)",
                    "accion_sugerida": "Aplicar 20% de descuento",
                    "prioridad": "MEDIA"
                })
        
        # 2. Productos con stock crítico (sugerir reposición)
        stock_critico = db.query(models.Producto).filter(
            models.Producto.stock_actual <= models.Producto.stock_minimo
        ).all()
        
        for producto in stock_critico:
            recomendaciones.append({
                "tipo": "REPOSICION_URGENTE",
                "producto_id": producto.id,
                "producto_nombre": producto.nombre,
                "categoria": producto.categoria,
                "motivo": f"Stock crítico ({producto.stock_actual} unidades, mínimo: {producto.stock_minimo})",
                "accion_sugerida": "Reponer stock inmediatamente",
                "prioridad": "ALTA" if producto.stock_actual == 0 else "MEDIA"
            })
        
        # 3. Productos estrella (sugerir aumentar stock)
        productos_estrella = db.query(
            models.Venta.producto_id,
            models.Producto.nombre,
            models.Producto.categoria,
            models.Producto.stock_actual,
            func.sum(models.Venta.cantidad).label("ventas_totales")
        ).join(models.Producto).filter(
            models.Venta.fecha >= datetime.now().date() - timedelta(days=30)
        ).group_by(models.Venta.producto_id, models.Producto.nombre, models.Producto.categoria, models.Producto.stock_actual
        ).order_by(func.sum(models.Venta.cantidad).desc()).limit(5).all()
        
        for producto in productos_estrella:
            if producto.stock_actual < 20:
                recomendaciones.append({
                    "tipo": "AUMENTAR_STOCK",
                    "producto_id": producto.producto_id,
                    "producto_nombre": producto.nombre,
                    "categoria": producto.categoria,
                    "motivo": f"Alta demanda ({producto.ventas_totales} ventas en 30 días), stock bajo: {producto.stock_actual}",
                    "accion_sugerida": "Aumentar stock en próximo pedido",
                    "prioridad": "MEDIA"
                })
        
        return recomendaciones
    
    @staticmethod
    def get_prediccion_ventas_simple(db: Session, categoria: str = None):
        """Predicción simple basada en promedio de últimos 3 meses"""
        tres_meses_atras = datetime.now().date() - timedelta(days=90)
        
        query = db.query(
            models.Producto.categoria,
            func.avg(models.Venta.cantidad).label("promedio_mensual"),
            func.count(models.Venta.id).label("total_ventas")
        ).join(models.Venta).filter(
            models.Venta.fecha >= tres_meses_atras
        )
        
        if categoria:
            query = query.filter(models.Producto.categoria == categoria)
        
        resultados = query.group_by(models.Producto.categoria).all()
        
        predicciones = []
        for r in resultados:
            # Predicción: promedio mensual * 1.1 (crecimiento del 10%)
            prediccion = round(float(r.promedio_mensual) * 1.1, 2) if r.promedio_mensual else 0
            
            predicciones.append({
                "categoria": r.categoria,
                "promedio_ventas_mensual": float(r.promedio_mensual) if r.promedio_mensual else 0,
                "total_ventas_3_meses": r.total_ventas,
                "prediccion_proximo_mes": prediccion,
                "tendencia": "CRECIMIENTO" if prediccion > (r.promedio_mensual or 0) else "ESTABLE"
            })
        
        return predicciones

