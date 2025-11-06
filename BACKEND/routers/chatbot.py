from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database.connection import get_db
from services.chatbot_service import ChatbotService
from utils.security import verify_api_key

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])

class MensajeChatbot(BaseModel):
    mensaje: str

class RespuestaChatbot(BaseModel):
    tipo: str
    respuesta: str
    datos: list
    sugerencias: Optional[list] = None

@router.post("/mensaje", response_model=RespuestaChatbot, dependencies=[Depends(verify_api_key)])
def enviar_mensaje_chatbot(
    mensaje: MensajeChatbot,
    db: Session = Depends(get_db)
):
    """
    Endpoint INNOVADOR: Chatbot inteligente para consultas en lenguaje natural
    
    Ejemplos de preguntas:
    - "¿Cuáles son los productos más vendidos?"
    - "¿Qué productos tienen stock bajo?"
    - "Muéstrame las ventas de la sucursal norte"
    - "Comparar ventas entre géneros"
    - "Dame recomendaciones"
    - "¿Cuáles son nuestras sucursales?"
    """
    try:
        respuesta = ChatbotService.procesar_mensaje(mensaje.mensaje, db)
        return respuesta
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar mensaje: {str(e)}"
        )

@router.get("/ejemplos")
def obtener_ejemplos_chatbot():
    """Obtiene ejemplos de preguntas que puede responder el chatbot"""
    return {
        "titulo": "Ejemplos de preguntas para el chatbot",
        "ejemplos": [
            {
                "categoria": "Productos Populares",
                "preguntas": [
                    "¿Cuáles son los productos más vendidos?",
                    "Muéstrame los productos más populares",
                    "Top productos de noviembre",
                    "Productos más vendidos de jeans"
                ]
            },
            {
                "categoria": "Inventario",
                "preguntas": [
                    "¿Qué productos tienen stock bajo?",
                    "Alertas de inventario",
                    "¿Hay productos agotados?",
                    "Stock disponible"
                ]
            },
            {
                "categoria": "Sucursales",
                "preguntas": [
                    "¿Cuáles son nuestras sucursales?",
                    "Ventas de la sucursal norte",
                    "Información de tiendas",
                    "Sucursales activas"
                ]
            },
            {
                "categoria": "Comparativos",
                "preguntas": [
                    "Comparar ventas entre géneros",
                    "Diferencia de ventas mujer vs hombre",
                    "Comparativo por género"
                ]
            },
            {
                "categoria": "Recomendaciones",
                "preguntas": [
                    "¿Qué me recomiendas?",
                    "Dame sugerencias",
                    "¿Qué acciones debería tomar?",
                    "Recomendaciones para mi negocio"
                ]
            }
        ],
        "nota": "El chatbot usa procesamiento de lenguaje natural simple para entender tus preguntas"
    }

