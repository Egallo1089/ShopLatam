@echo off
echo =======================================================
echo 🛑 DETENIENDO SERVIDOR BACKEND (MATA PROCESOS DE PYTHON)
echo =======================================================
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1

echo.
echo =======================================================
echo 🗑️  BORRANDO BASE DE DATOS Y USUARIOS ANTERIORES
echo =======================================================
del /F /Q "backend\shoplatam_local.db" >nul 2>&1

echo.
echo ✅ TODO HA SIDO BORRADO EXITOSAMENTE.
echo.
echo =======================================================
echo 🚀 AHORA INICIA TU SERVIDOR PARA CREAR NUEVOS USUARIOS
echo =======================================================
echo 1. Abre tu terminal de backend y escribe:
echo    cd backend
echo    python main_local.py
echo.
echo 2. El servidor iniciara, creara una nueva base de datos y
echo    creara tus usuarios de prueba:
echo    Admin: admin@shoplatam.com / Admin2026!
echo    Demo:  demo@shoplatam.com / demo1234
echo.
pause
