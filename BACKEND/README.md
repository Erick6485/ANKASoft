# Retail Analytics Backend

Backend API para análisis de retail desarrollado para la hackatón.

## Descripción

Sistema backend construido con FastAPI para proporcionar servicios de análisis de datos de retail.

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos principal
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Estructura del Proyecto

```
retail-analytics-backend/
├── database/           # Modelos y configuración de base de datos
├── routers/           # Endpoints de la API
├── services/          # Lógica de negocio
├── utils/             # Utilidades y helpers
├── main.py            # Archivo principal de la aplicación
├── requirements.txt   # Dependencias del proyecto
├── .env              # Variables de entorno (no incluir en git)
├── .gitignore        # Archivos ignorados por git
└── README.md         # Este archivo
```

## Instalación
1. python -m venv venv
2. source venv/bin/activate  # o venv\Scripts\activate en Windows
3. pip install -r requirements.txt

## Endpoints Disponibles

- `GET /` - Endpoint de bienvenida
- `GET /health` - Verificación de salud del servicio
- `GET /docs` - Documentación interactiva (Swagger UI)
- `GET /redoc` - Documentación alternativa (ReDoc)

## Desarrollo

### Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Desactivar entorno virtual
```bash
deactivate
```

## Agregar nuevas dependencias

```bash
pip install nombre-paquete
pip freeze > requirements.txt
```

## Testing

```bash
pytest
```

## Equipo

Desarrollado para la Hackatón.

## Licencia

Este proyecto es parte de una hackatón.

---

**Nota:** Recuerda actualizar el archivo `.env` con tus configuraciones específicas antes de ejecutar el proyecto.

