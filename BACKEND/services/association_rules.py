from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import itertools
from database import models

class AssociationRulesService:
    
    @staticmethod
    def encontrar_reglas_asociacion(db: Session, confianza_minima: float = 0.5, soporte_minimo: float = 0.1):
        """
        Encuentra reglas de asociación usando algoritmo Apriori simplificado
        Ej: {Camiseta} → {Jeans} (confianza: 65%)
        """
        
        # Obtener transacciones (ventas agrupadas por ticket/compra)
        # Para simplificar, agrupamos ventas del mismo día y sucursal como una "compra"
        transacciones = db.query(
            func.date(models.Venta.fecha).label('fecha_compra'),
            models.Venta.sucursal_id,
            models.Producto.categoria
        ).join(models.Producto).group_by(
            func.date(models.Venta.fecha), 
            models.Venta.sucursal_id, 
            models.Producto.categoria
        ).all()
        
        # Crear itemsets (productos vendidos juntos)
        compras_por_dia_sucursal = defaultdict(list)
        
        for transaccion in transacciones:
            clave = f"{transaccion.fecha_compra}_{transaccion.sucursal_id}"
            compras_por_dia_sucursal[clave].append(transaccion.categoria)
        
        # Convertir a lista de transacciones
        transacciones_lista = list(compras_por_dia_sucursal.values())
        total_transacciones = len(transacciones_lista)
        
        if total_transacciones == 0:
            return []
        
        # Encontrar itemsets frecuentes
        itemsets_frecuentes = AssociationRulesService._encontrar_itemsets_frecuentes(
            transacciones_lista, soporte_minimo, total_transacciones
        )
        
        # Generar reglas de asociación
        reglas = AssociationRulesService._generar_reglas(
            itemsets_frecuentes, transacciones_lista, confianza_minima, total_transacciones
        )
        
        return reglas
    
    @staticmethod
    def _encontrar_itemsets_frecuentes(transacciones: List[List[str]], soporte_minimo: float, total_transacciones: int):
        """Encuentra itemsets que cumplen con el soporte mínimo"""
        conteo_items = Counter()
        
        # Contar frecuencia de items individuales
        for transaccion in transacciones:
            for item in set(transaccion):  # Usar set para evitar duplicados en misma transacción
                conteo_items[frozenset([item])] += 1
        
        # Filtrar por soporte mínimo
        itemsets_frecuentes = {}
        itemsets_frecuentes[1] = {
            itemset: count / total_transacciones
            for itemset, count in conteo_items.items()
            if count / total_transacciones >= soporte_minimo
        }
        
        # Itemsets de tamaño 2
        k = 2
        while True:
            candidatos = AssociationRulesService._generar_candidatos(itemsets_frecuentes[k-1])
            if not candidatos:
                break
            
            conteo_candidatos = Counter()
            for transaccion in transacciones:
                items_transaccion = set(transaccion)
                for candidato in candidatos:
                    if candidato.issubset(items_transaccion):
                        conteo_candidatos[candidato] += 1
            
            # Filtrar por soporte mínimo
            itemsets_frecuentes[k] = {
                itemset: count / total_transacciones
                for itemset, count in conteo_candidatos.items()
                if count / total_transacciones >= soporte_minimo
            }
            
            if not itemsets_frecuentes[k]:
                break
            
            k += 1
        
        return itemsets_frecuentes
    
    @staticmethod
    def _generar_candidatos(itemsets_previos: Dict):
        """Genera candidatos para el siguiente nivel"""
        candidatos = set()
        itemsets_lista = list(itemsets_previos.keys())
        
        for i in range(len(itemsets_lista)):
            for j in range(i + 1, len(itemsets_lista)):
                itemset1 = itemsets_lista[i]
                itemset2 = itemsets_lista[j]
                
                # Unir itemsets si comparten todos los elementos excepto el último
                if len(itemset1.union(itemset2)) == len(itemset1) + 1:
                    candidato = itemset1.union(itemset2)
                    candidatos.add(candidato)
        
        return candidatos
    
    @staticmethod
    def _generar_reglas(itemsets_frecuentes: Dict, transacciones: List[List[str]], confianza_minima: float, total_transacciones: int):
        """Genera reglas de asociación desde itemsets frecuentes"""
        reglas = []
        
        for tamaño, itemsets in itemsets_frecuentes.items():
            if tamaño < 2:
                continue
            
            for itemset, soporte in itemsets.items():
                # Generar todas las posibles reglas
                for antecedente in itertools.combinations(itemset, tamaño - 1):
                    antecedente_set = frozenset(antecedente)
                    consecuente = itemset - antecedente_set
                    
                    # Calcular confianza
                    soporte_antecedente = AssociationRulesService._calcular_soporte(antecedente_set, transacciones, total_transacciones)
                    confianza = soporte / soporte_antecedente if soporte_antecedente > 0 else 0
                    
                    if confianza >= confianza_minima:
                        reglas.append({
                            "antecedente": list(antecedente_set),
                            "consecuente": list(consecuente),
                            "soporte": round(soporte * 100, 2),  # Porcentaje
                            "confianza": round(confianza * 100, 2),  # Porcentaje
                            "lift": round(confianza / soporte, 2) if soporte > 0 else 0
                        })
        
        # Ordenar por confianza descendente
        reglas.sort(key=lambda x: x["confianza"], reverse=True)
        return reglas[:10]  # Devolver solo top 10 reglas
    
    @staticmethod
    def _calcular_soporte(itemset, transacciones: List[List[str]], total_transacciones: int):
        """Calcula el soporte de un itemset"""
        count = 0
        for transaccion in transacciones:
            if itemset.issubset(set(transaccion)):
                count += 1
        return count / total_transacciones if total_transacciones > 0 else 0
    
    @staticmethod
    def get_recomendaciones_cruzadas(db: Session, producto_categoria: str):
        """Obtiene recomendaciones cruzadas basadas en reglas de asociación"""
        reglas = AssociationRulesService.encontrar_reglas_asociacion(db)
        
        recomendaciones = []
        for regla in reglas:
            if producto_categoria in regla["antecedente"]:
                # Producto está en antecedente, recomendar consecuente
                for producto_recomendado in regla["consecuente"]:
                    if producto_recomendado != producto_categoria:
                        recomendaciones.append({
                            "producto_actual": producto_categoria,
                            "producto_recomendado": producto_recomendado,
                            "confianza": f"{regla['confianza']}%",
                            "explicacion": f"Los clientes que compran {producto_categoria} también compran {producto_recomendado} en el {regla['confianza']}% de los casos"
                        })
            elif producto_categoria in regla["consecuente"]:
                # Producto está en consecuente, recomendar antecedente
                for producto_recomendado in regla["antecedente"]:
                    if producto_recomendado != producto_categoria:
                        recomendaciones.append({
                            "producto_actual": producto_categoria,
                            "producto_recomendado": producto_recomendado,
                            "confianza": f"{regla['confianza']}%",
                            "explicacion": f"Los clientes que compran {producto_recomendado} también compran {producto_categoria} en el {regla['confianza']}% de los casos"
                        })
        
        # Eliminar duplicados y devolver top 5
        recomendaciones_unicas = []
        vistas = set()
        for rec in recomendaciones:
            key = (rec["producto_actual"], rec["producto_recomendado"])
            if key not in vistas:
                vistas.add(key)
                recomendaciones_unicas.append(rec)
        
        return recomendaciones_unicas[:5]

