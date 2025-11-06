from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional

# API Key simple para la demo - En producción usar variables de entorno
API_KEY = "retail_hackaton_2025_fup"

# Definir el esquema de seguridad para Swagger UI
api_key_header_scheme = APIKeyHeader(
    name="X-API-Key",
    description="API Key para acceder a los endpoints protegidos. Usa: retail_hackaton_2025_fup"
)

def verify_api_key(api_key: str = Security(api_key_header_scheme)):
    """Middleware simple para verificar API Key"""
    if not api_key:
        raise HTTPException(
            status_code=401, 
            detail="API Key requerida. Usa el header: X-API-Key con el valor: retail_hackaton_2025_fup"
        )
    
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="API Key inválida. Usa: retail_hackaton_2025_fup"
        )
    
    return api_key

