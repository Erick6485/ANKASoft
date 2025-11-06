from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import database.models as models
from database.connection import engine
from contextlib import asynccontextmanager

# Importar routers
from routers import analytics, chatbot, auth, inventario, ventas, kpis, reportes

# Configurar esquema de seguridad para Swagger UI
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Crear tablas en la base de datos al iniciar
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Retail Analytics API",
    description="API para análisis de ventas e inventario de retail de ropa",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)

# Configurar CORS para conectar con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(analytics.router)
app.include_router(chatbot.router)
app.include_router(inventario.router)
app.include_router(ventas.router)
app.include_router(kpis.router)
app.include_router(reportes.router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Retail Analytics API - Hackatón 2025", 
        "docs": "/docs",
        "version": "1.0.0",
        "autenticacion": {
            "tipo": "API Key",
            "header": "X-API-Key",
            "api_key": "retail_hackaton_2025_fup",
            "nota": "Todos los endpoints de analytics requieren API Key"
        },
        "endpoints_principales": {
            "autenticacion": [
                "/api/auth/register 📝 (Registrarse)",
                "/api/auth/login 🔐 (Iniciar sesión)",
                "/api/auth/login-json 🔐 (Login alternativo)",
                "/api/auth/me 👤 (Mi perfil)"
            ],
            "analytics_basicos": [
                "/api/analytics/productos-mas-vendidos 🔒",
                "/api/analytics/rotacion-tallas 🔒", 
                "/api/analytics/alertas-stock 🔒",
                "/api/analytics/comparativo-generos 🔒"
            ],
            "analytics_innovadores": [
                "/api/analytics/recomendaciones-inteligentes 🔒🆕",
                "/api/analytics/prediccion-ventas 🔒🆕", 
                "/api/analytics/dashboard-resumen 🔒🆕",
                "/api/analytics/reglas-asociacion 🔒🆕🔥",
                "/api/analytics/recomendaciones-cruzadas/{categoria} 🔒🆕🔥"
            ],
            "chatbot_ia": [
                "/api/chatbot/mensaje 🔒🤖⭐ (Lenguaje natural)",
                "/api/chatbot/ejemplos 📚 (sin autenticación)"
            ],
            "utilidades_publicas": [
                "/api/analytics/cargar-datos-ejemplo (sin autenticación)"
            ]
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "retail-analytics-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

