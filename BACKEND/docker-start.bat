@echo off
REM Script para iniciar el proyecto con Docker
REM Retail Analytics - Hackaton 2025

echo ==========================================
echo INICIANDO RETAIL ANALYTICS CON DOCKER
echo ==========================================
echo.

REM Verificar que Docker este instalado
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker no esta instalado
    echo Descarga desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose no esta instalado
    pause
    exit /b 1
)

echo ✅ Docker encontrado
echo.

REM Construir y levantar contenedores
echo [1/4] Construyendo imagenes...
docker-compose build

echo.
echo [2/4] Iniciando contenedores...
docker-compose up -d

echo.
echo [3/4] Esperando que la base de datos este lista...
timeout /t 10 /nobreak >nul

echo.
echo [4/4] Cargando datos de ejemplo...
docker-compose exec backend python cargar_datos.py

echo.
echo ==========================================
echo ✅ PROYECTO INICIADO EXITOSAMENTE
echo ==========================================
echo.
echo URLs disponibles:
echo   🌐 API:            http://localhost:8000
echo   📚 Documentacion:  http://localhost:8000/docs
echo   ❤  Health:         http://localhost:8000/health
echo.
echo API Key para autenticacion:
echo   🔑 retail_hackaton_2025_fup
echo.
echo Comandos utiles:
echo   Ver logs:      docker-compose logs -f
echo   Detener:       docker-compose down
echo   Reiniciar:     docker-compose restart
echo.
echo ==========================================
echo.
pause

