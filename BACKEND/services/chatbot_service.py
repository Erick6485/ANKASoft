from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import re
from datetime import datetime, timedelta
from database import models
from services.analytics_service import AnalyticsService
from services.association_rules import AssociationRulesService

class ChatbotService:
    
    @staticmethod
    def procesar_mensaje(mensaje: str, db: Session):
        """Procesa el mensaje del usuario y devuelve respuesta inteligente"""
        mensaje = mensaje.lower().strip()
        
        # Detectar intención y extraer parámetros
        intencion = ChatbotService._detectar_intencion(mensaje)
        parametros = ChatbotService._extraer_parametros(mensaje)
        
        if intencion == "productos_populares":
            return ChatbotService._obtener_productos_populares(db, parametros)
        elif intencion == "stock_alerts":
            return ChatbotService._obtener_alertas_stock(db, parametros)
        elif intencion == "ventas_sucursal":
            return ChatbotService._obtener_ventas_sucursal(db, parametros)
        elif intencion == "comparativo":
            return ChatbotService._obtener_comparativo(db, parametros)
        elif intencion == "recomendaciones":
            return ChatbotService._obtener_recomendaciones(db)
        elif intencion == "sucursales":
            return ChatbotService._obtener_sucursales(db)
        elif intencion == "reglas_asociacion":
            return ChatbotService._obtener_reglas_asociacion(db, parametros)
        else:
            return ChatbotService._respuesta_por_defecto()

    @staticmethod
    def _detectar_intencion(mensaje: str):
        """Detecta la intención del usuario basado en palabras clave"""
        palabras = mensaje.split()
        
        if any(palabra in mensaje for palabra in ['más vendido', 'popular', 'top', 'mejor']):
            return "productos_populares"
        elif any(palabra in mensaje for palabra in ['stock', 'inventario', 'agotado', 'disponible']):
            return "stock_alerts"
        elif any(palabra in mensaje for palabra in ['sucursal', 'tienda', 'local', 'ventas por tienda']):
            return "ventas_sucursal"
        elif any(palabra in mensaje for palabra in ['comparar', 'vs', 'versus', 'diferencia']):
            return "comparativo"
        elif any(palabra in mensaje for palabra in ['recomendación', 'sugerencia', 'acción', 'debería']):
            return "recomendaciones"
        elif any(palabra in mensaje for palabra in ['sucursales', 'tiendas', 'locales']):
            return "sucursales"
        elif any(palabra in mensaje for palabra in ['también compran', 'compran juntos', 'relacionados', 'combo', 'patrones']):
            return "reglas_asociacion"
        else:
            return "desconocido"

    @staticmethod
    def _extraer_parametros(mensaje: str):
        """Extrae parámetros del mensaje (sucursal, categoría, etc.)"""
        parametros = {}
        
        # Detectar sucursales
        sucursales_keywords = {
            'norte': 'Sucursal Norte',
            'sur': 'Sucursal Sur', 
            'centro': 'Sucursal Centro',
            'este': 'Sucursal Este',
            'oeste': 'Sucursal Oeste'
        }
        
        for keyword, sucursal in sucursales_keywords.items():
            if keyword in mensaje:
                parametros['sucursal'] = sucursal
                break
        
        # Detectar categorías
        categorias_keywords = ['camiseta', 'jeans', 'pantalón', 'vestido', 'abrigo', 'bermuda', 'buzo']
        for categoria in categorias_keywords:
            if categoria in mensaje:
                parametros['categoria'] = categoria.upper()
                break
        
        # Detectar géneros
        if 'mujer' in mensaje:
            parametros['genero'] = 'mujer'
        elif 'hombre' in mensaje:
            parametros['genero'] = 'hombre'
        elif 'niño' in mensaje:
            parametros['genero'] = 'niño'
        elif 'niña' in mensaje:
            parametros['genero'] = 'niña'
        
        # Detectar meses
        meses_keywords = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        
        for mes, numero in meses_keywords.items():
            if mes in mensaje:
                parametros['mes'] = numero
                break
        
        return parametros

    @staticmethod
    def _obtener_productos_populares(db: Session, parametros: dict):
        """Obtiene productos populares basado en parámetros"""
        resultados = AnalyticsService.get_productos_mas_vendidos(
            db, 
            mes=parametros.get('mes'),
            categoria=parametros.get('categoria'),
            limite=5
        )
        
        if not resultados:
            return {
                "tipo": "productos_populares",
                "respuesta": "No encontré productos con esos filtros. ¿Quieres intentar con otros parámetros?",
                "datos": []
            }
        
        productos = []
        for r in resultados:
            productos.append({
                "producto": r.nombre,
                "categoria": r.categoria,
                "talla": r.talla,
                "vendidos": int(r.total_vendido),
                "ingresos": f"${r.ingreso_total:,.2f}"
            })
        
        return {
            "tipo": "productos_populares",
            "respuesta": f"🔝 Estos son los productos más populares{' ' + parametros.get('categoria', '').lower() if parametros.get('categoria') else ''}:",
            "datos": productos
        }

    @staticmethod
    def _obtener_alertas_stock(db: Session, parametros: dict):
        """Obtiene alertas de stock"""
        alertas = AnalyticsService.get_stock_alerts(db)
        
        if not alertas:
            return {
                "tipo": "stock_alerts", 
                "respuesta": "✅ Todo en orden! No hay productos con stock crítico.",
                "datos": []
            }
        
        productos_alerta = []
        for producto in alertas[:5]:  # Solo primeros 5
            productos_alerta.append({
                "producto": producto.nombre,
                "categoria": producto.categoria,
                "stock_actual": producto.stock_actual,
                "stock_minimo": producto.stock_minimo,
                "estado": "AGOTADO" if producto.stock_actual == 0 else "BAJO"
            })
        
        return {
            "tipo": "stock_alerts",
            "respuesta": f"🚨 Encontré {len(alertas)} productos con stock crítico:",
            "datos": productos_alerta
        }
    
    @staticmethod
    def _obtener_ventas_sucursal(db: Session, parametros: dict):
        """Obtiene ventas por sucursal"""
        sucursal_nombre = parametros.get('sucursal')
        
        if sucursal_nombre:
            sucursal = db.query(models.Sucursal).filter(
                models.Sucursal.nombre == sucursal_nombre
            ).first()
            
            if not sucursal:
                return {
                    "tipo": "ventas_sucursal",
                    "respuesta": f"No encontré la sucursal '{sucursal_nombre}'",
                    "datos": []
                }
            
            ventas = db.query(models.Venta).filter(
                models.Venta.sucursal_id == sucursal.id
            ).count()
            
            return {
                "tipo": "ventas_sucursal",
                "respuesta": f"📊 La {sucursal_nombre} tiene {ventas} ventas registradas",
                "datos": [{"sucursal": sucursal_nombre, "total_ventas": ventas}]
            }
        else:
            # Mostrar todas las sucursales
            return ChatbotService._obtener_sucursales(db)
    
    @staticmethod
    def _obtener_comparativo(db: Session, parametros: dict):
        """Obtiene comparativo entre géneros"""
        resultados = AnalyticsService.get_comparativo_generos(db)
        
        comparativo = []
        for r in resultados:
            comparativo.append({
                "genero": r.genero_cliente.value if hasattr(r.genero_cliente, 'value') else str(r.genero_cliente),
                "unidades": int(r.total_unidades) if r.total_unidades else 0,
                "ingresos": f"${r.total_ingresos:,.2f}" if r.total_ingresos else "$0.00"
            })
        
        return {
            "tipo": "comparativo",
            "respuesta": "📊 Comparativo de ventas por género:",
            "datos": comparativo
        }

    @staticmethod
    def _obtener_sucursales(db: Session):
        """Obtiene información de sucursales"""
        sucursales = db.query(models.Sucursal).filter(models.Sucursal.activa == True).all()
        
        if not sucursales:
            return {
                "tipo": "sucursales",
                "respuesta": "No hay sucursales registradas en el sistema.",
                "datos": []
            }
        
        datos_sucursales = []
        for sucursal in sucursales:
            # Contar ventas de la sucursal
            total_ventas = db.query(models.Venta).filter(
                models.Venta.sucursal_id == sucursal.id
            ).count()
            
            datos_sucursales.append({
                "nombre": sucursal.nombre,
                "ciudad": sucursal.ciudad,
                "direccion": sucursal.direccion,
                "telefono": sucursal.telefono,
                "ventas_totales": total_ventas
            })
        
        return {
            "tipo": "sucursales",
            "respuesta": f"🏪 Tenemos {len(sucursales)} sucursales activas:",
            "datos": datos_sucursales
        }

    @staticmethod
    def _obtener_recomendaciones(db: Session):
        """Obtiene recomendaciones inteligentes"""
        recomendaciones = AnalyticsService.get_recomendaciones_inteligentes(db)
        
        if not recomendaciones:
            return {
                "tipo": "recomendaciones",
                "respuesta": "No tengo recomendaciones específicas en este momento.",
                "datos": []
            }
        
        return {
            "tipo": "recomendaciones",
            "respuesta": f"💡 Tengo {len(recomendaciones)} recomendaciones para optimizar tu negocio:",
            "datos": recomendaciones[:3]  # Solo 3 recomendaciones
        }

    @staticmethod
    def _obtener_reglas_asociacion(db: Session, parametros: dict):
        """Obtiene reglas de asociación de productos"""
        reglas = AssociationRulesService.encontrar_reglas_asociacion(db)
        
        if not reglas:
            return {
                "tipo": "reglas_asociacion",
                "respuesta": "No encontré patrones de compra significativos en los datos actuales.",
                "datos": []
            }
        
        reglas_simplificadas = []
        for regla in reglas[:3]:  # Solo mostrar top 3
            reglas_simplificadas.append({
                "regla": f"Quienes compran {', '.join(regla['antecedente'])} también compran {', '.join(regla['consecuente'])}",
                "confianza": f"{regla['confianza']}%",
                "frecuencia": f"{regla['soporte']}% de las compras"
            })
        
        return {
            "tipo": "reglas_asociacion", 
            "respuesta": "🔍 Patrones de compra descubiertos:",
            "datos": reglas_simplificadas
        }
    
    @staticmethod
    def _respuesta_por_defecto():
        """Respuesta cuando no se entiende el mensaje"""
        return {
            "tipo": "ayuda",
            "respuesta": "🤖 Hola! Soy tu asistente de retail. Puedo ayudarte con:",
            "sugerencias": [
                "📊 \"Productos más vendidos\"",
                "🚨 \"Alertas de stock\"", 
                "🏪 \"Ventas por sucursal\"",
                "👥 \"Comparar géneros\"",
                "💡 \"Recomendaciones\"",
                "📍 \"Sucursales\"",
                "🔍 \"Productos que compran juntos\""
            ]
        }

