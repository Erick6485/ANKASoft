@echo off
REM =====================================================
REM Script para exportar la base de datos PostgreSQL
REM Retail Analytics - Hackatón 2025
REM =====================================================

echo ==========================================
echo EXPORTANDO BASE DE DATOS
echo ==========================================
echo.

REM Configuración
set DB_NAME=retail_analytics
set DB_USER=postgres
set OUTPUT_SCHEMA=database\export_schema.sql
set OUTPUT_DATA=database\sample_data.sql

REM Solicitar contraseña
set /p PASSWORD="Ingresa la contraseña de postgres: "

echo.
echo [1/2] Exportando esquema...
echo.

REM Exportar solo el esquema (estructura)
pg_dump -U %DB_USER% -d %DB_NAME% --schema-only --no-owner --no-privileges > %OUTPUT_SCHEMA%

if %ERRORLEVEL% == 0 (
    echo ✓ Esquema exportado a: %OUTPUT_SCHEMA%
) else (
    echo ✗ Error al exportar esquema
    echo Verifica que PostgreSQL este instalado y en PATH
    pause
    exit /b 1
)

echo.
echo [2/2] Exportando datos de ejemplo (opcional)...
echo.

REM Exportar datos (solo primeros 100 registros)
pg_dump -U %DB_USER% -d %DB_NAME% --data-only --no-owner --no-privileges 2>nul | findstr /N "." | head -100 > %OUTPUT_DATA%

if %ERRORLEVEL% == 0 (
    echo ✓ Datos de ejemplo exportados
) else (
    echo ⚠ Datos de ejemplo no exportados (opcional)
)

echo.
echo ==========================================
echo EXPORTACION COMPLETADA
echo ==========================================
echo.
echo Archivos generados:
echo   - %OUTPUT_SCHEMA%
echo   - %OUTPUT_DATA%
echo.
echo Ahora puedes agregar estos archivos a Git:
echo   git add database\export_schema.sql
echo   git commit -m "docs: Agregar esquema de base de datos"
echo.
pause

