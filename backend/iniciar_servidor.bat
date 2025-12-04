@echo off
echo ============================================
echo   SERVIDOR API - APPTELINK VISION
echo ============================================
echo.

cd /d "%~dp0"

REM Intentar con diferentes versiones de Python
set PYTHON_PATH=

REM Buscar Python 3.11
if exist "C:\Program Files\Python311\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python311\python.exe
    goto :found
)

REM Buscar Python 3.12
if exist "C:\Program Files\Python312\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python312\python.exe
    goto :found
)

REM Buscar Python en AppData
for /d %%i in ("C:\Users\Administrator\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_PATH=%%i\python.exe
        goto :found
    )
)

REM Usar python del PATH
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    set PYTHON_PATH=python
    goto :found
)

echo ERROR: No se encontro Python instalado
pause
exit /b 1

:found
echo Python: %PYTHON_PATH%
echo.
echo Iniciando servidor en http://localhost:5000
echo Presiona Ctrl+C para detener
echo.
"%PYTHON_PATH%" server.py
pause

