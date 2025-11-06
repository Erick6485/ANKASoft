#!/bin/bash
# Script para iniciar el proyecto con Docker
# Retail Analytics - Hackatón 2025

echo "=========================================="
echo "INICIANDO RETAIL ANALYTICS CON DOCKER"
echo "=========================================="
echo ""

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "Descarga desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker encontrado"
echo ""

# Construir y levantar contenedores
echo "[1/4] Construyendo imágenes..."
docker-compose build

echo ""
echo "[2/4] Iniciando contenedores..."
docker-compose up -d

echo ""
echo "[3/4] Esperando que la base de datos esté lista..."
sleep 10

echo ""
echo "[4/4] Cargando datos de ejemplo..."
docker-compose exec backend python cargar_datos.py

echo ""
echo "=========================================="
echo "✅ PROYECTO INICIADO EXITOSAMENTE"
echo "=========================================="
echo ""
echo "URLs disponibles:"
echo "  🌐 API:            http://localhost:8000"
echo "  📚 Documentación:  http://localhost:8000/docs"
echo "  ❤️  Health:         http://localhost:8000/health"
echo ""
echo "API Key para autenticación:"
echo "  🔑 retail_hackaton_2025_fup"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:      docker-compose logs -f"
echo "  Detener:       docker-compose down"
echo "  Reiniciar:     docker-compose restart"
echo ""
echo "=========================================="

