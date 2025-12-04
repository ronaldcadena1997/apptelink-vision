@echo off
echo ============================================
echo   INSTALANDO DEPENDENCIAS - APPTELINK API
echo ============================================
echo.

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
echo Python encontrado: %PYTHON_PATH%
echo.
echo Instalando Flask y dependencias...
"%PYTHON_PATH%" -m pip install --upgrade pip
"%PYTHON_PATH%" -m pip install flask flask-cors opencv-python

echo.
echo ============================================
echo   INSTALACION COMPLETADA
echo ============================================
pause

