#!/bin/bash
# =====================================================
# Script para exportar la base de datos PostgreSQL
# Retail Analytics - Hackatón 2025
# =====================================================

echo "=========================================="
echo "EXPORTANDO BASE DE DATOS"
echo "=========================================="
echo ""

# Configuración
DB_NAME="retail_analytics"
DB_USER="postgres"
OUTPUT_SCHEMA="database/export_schema.sql"
OUTPUT_DATA="database/sample_data.sql"

# Exportar solo el esquema (estructura)
echo "[1/2] Exportando esquema..."
pg_dump -U $DB_USER -d $DB_NAME --schema-only --no-owner --no-privileges > $OUTPUT_SCHEMA

if [ $? -eq 0 ]; then
    echo "✓ Esquema exportado a: $OUTPUT_SCHEMA"
else
    echo "✗ Error al exportar esquema"
    exit 1
fi

# Exportar datos de ejemplo (opcional, solo algunos registros)
echo ""
echo "[2/2] Exportando datos de ejemplo..."
pg_dump -U $DB_USER -d $DB_NAME --data-only --no-owner --no-privileges | head -100 > $OUTPUT_DATA

if [ $? -eq 0 ]; then
    echo "✓ Datos de ejemplo exportados a: $OUTPUT_DATA"
else
    echo "⚠ No se pudieron exportar datos (opcional)"
fi

echo ""
echo "=========================================="
echo "EXPORTACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Archivos generados:"
echo "  - $OUTPUT_SCHEMA"
echo "  - $OUTPUT_DATA"
echo ""
echo "Ahora puedes agregar estos archivos a Git:"
echo "  git add database/export_schema.sql"
echo "  git commit -m 'docs: Agregar esquema de base de datos'"
echo ""

