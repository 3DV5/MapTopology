@echo off
chcp 65001 > nul
echo ========================================
echo    SETUP COMPLETO - MapTopologia
echo ========================================
echo.

echo 1. Parando processos Python...
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im pythonw.exe /t >nul 2>&1

echo.
echo 2. Deletando venv antigo (se existir)...
if exist "venv" (
    echo   🗑️  Removendo venv antigo...
    rmdir /s /q venv
)

echo.
echo 3. Criando NOVO venv...
python -m venv venv
if errorlevel 1 (
    echo   ❌ Erro ao criar venv!
    pause
    exit /b 1
)

echo.
echo 4. Ativando venv...
call venv\Scripts\activate.bat

echo.
echo 5. Verificando se venv esta ativo...
python -c "import sys; print('   ✅ Venv ativo!' if 'venv' in sys.prefix else '   ❌ Venv NAO ativo!')"

echo.
echo 6. Atualizando pip...
python -m pip install --upgrade pip

echo.
echo 7. Instalando TODAS as dependencias no VENV...
echo.
pip install customtkinter==5.2.0
pip install Pillow==10.0.1
pip install scapy==2.5.0
pip install networkx==3.1
pip install matplotlib==3.7.2
pip install reportlab==4.0.4
pip install python-nmap==0.7.1

echo.
echo 8. Verificando instalacoes no VENV...
echo.
python -c "try: import scapy; print('✅ scapy OK'); except: print('❌ scapy FALHOU')"
python -c "try: import customtkinter; print('✅ customtkinter OK'); except: print('❌ customtkinter FALHOU')"
python -c "try: import networkx; print('✅ networkx OK'); except: print('❌ networkx FALHOU')"
python -c "try: import reportlab; print('✅ reportlab OK'); except: print('❌ reportlab FALHOU')"
python -c "try: import nmap; print('✅ python-nmap OK'); except: print('❌ python-nmap FALHOU')"
python -c "try: from PIL import Image; print('✅ Pillow OK'); except: print('❌ Pillow FALHOU')"
python -c "try: import matplotlib; print('✅ matplotlib OK'); except: print('❌ matplotlib FALHOU')"

echo.
echo ========================================
echo    ✅ SETUP CONCLUIDO!
echo ========================================
echo.
echo Agora execute: python main.py
echo.
pause