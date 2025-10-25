import sys
import os

def verificar_modulo(nome):
    try:
        __import__(nome)
        return "✅ OK"
    except ImportError:
        return "❌ FALHOU"

print("=== VERIFICACAO DO VENV ===")
print(f"Python: {sys.executable}")
print(f"Venv ativo: {'venv' in sys.prefix}")
print(f"Diretorio: {os.getcwd()}")
print()

modulos = ["scapy", "customtkinter", "networkx", "reportlab", "nmap", "PIL", "matplotlib"]

print("MODULOS INSTALADOS:")
for modulo in modulos:
    status = verificar_modulo(modulo)
    print(f"  {modulo:15} {status}")

print()
if "venv" in sys.prefix:
    print("🎉 VENV ATIVO! Tudo pronto para executar.")
    print("Execute: python main.py")
else:
    print("⚠️  VENV NAO ATIVO!")
    print("Execute: venv\\Scripts\\activate.bat")

input("\nPressione Enter para sair...")