@echo off
chcp 65001 > nul
title MapTopologia - Sistema em Execucao

echo ========================================
echo    INICIANDO MAPTOPOLOGIA
echo ========================================
echo.

echo 1. Verificando e ativando VENV...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo   ✅ Venv ativado
) else (
    echo   ❌ Venv nao encontrado!
    echo   📦 Execute primeiro: setup_completo.bat
    pause
    exit /b 1
)

echo.
echo 2. Verificando se venv esta realmente ativo...
python -c "import sys; exit(0) if 'venv' in sys.prefix else exit(1)" >nul 2>&1
if errorlevel 1 (
    echo   ❌ ERRO: Venv nao esta ativo!
    echo   📋 Execute manualmente: venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo.
echo 3. Iniciando sistema MapTopologia...
python main.py

echo.
echo ========================================
echo    SISTEMA FINALIZADO
echo ========================================
echo.
pause