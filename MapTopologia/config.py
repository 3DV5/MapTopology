import os

class Config:
    # Configurações da aplicação
    APP_NAME = "MapTopologia"
    VERSION = "1.0.0"
    
    # Configurações de rede
    DEFAULT_NETWORK_RANGE = "192.168.1.0/24"
    SCAN_TIMEOUT = 2
    
    # Configurações de arquivo
    REPORTS_DIR = "reports"
    ASSETS_DIR = "assets"
    
    # Cores e tema
    THEME = "dark-blue"
    
    @classmethod
    def setup_directories(cls):
        """Cria diretórios necessários"""
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
        os.makedirs(cls.ASSETS_DIR, exist_ok=True)