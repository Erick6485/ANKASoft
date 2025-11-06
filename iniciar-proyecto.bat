@echo off
echo ==========================================
echo INICIANDO RETAIL ANALYTICS
echo Frontend + Backend
echo Hackaton 2025 - FUP
echo ==========================================
echo.

echo [1/2] Iniciando Backend...
echo.
start "Backend - Retail Analytics" cmd /k "cd BACKEND && .\venv\Scripts\activate && python main.py"

timeout /t 5 /nobreak >nul

echo [2/2] Iniciando Frontend...
echo.
start "Frontend - Retail Analytics" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo ✅ PROYECTO INICIADO
echo ==========================================
echo.
echo URLs disponibles:
echo   🎨 Frontend:  http://localhost:5173
echo   🔌 Backend:   http://localhost:8000
echo   📚 API Docs:  http://localhost:8000/docs
echo.
echo Usuarios de prueba:
echo   👤 admin / admin123
echo   👤 gerente / gerente123
echo   👤 vendedor / vendedor123
echo.
echo ==========================================
echo.
echo Se abrieron 2 ventanas nuevas:
echo   - Backend (Python)
echo   - Frontend (React)
echo.
echo Para detener: Cerrar ambas ventanas o CTRL+C
echo.
pause

