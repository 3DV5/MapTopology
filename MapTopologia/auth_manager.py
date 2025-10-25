class AuthManager:
    def __init__(self, database):
        self.database = database
        self.current_user = None
    
    def login(self, username, password):
        """Autentica usuário"""
        user = self.database.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            return True, f"Bem-vindo, {user['full_name']}!"
        else:
            return False, "Usuário ou senha incorretos!"
    
    def logout(self):
        """Desconecta usuário"""
        if self.current_user:
            user_name = self.current_user['full_name']
            self.current_user = None
            return True, f"Até logo, {user_name}!"
        return False, "Nenhum usuário logado!"
    
    def get_current_user(self):
        """Retorna usuário atual"""
        return self.current_user
    
    def is_authenticated(self):
        """Verifica se usuário está autenticado"""
        return self.current_user is not None
    
    def has_permission(self, required_role):
        """Verifica permissões"""
        if not self.current_user:
            return False
        return self.current_user["role"] == required_role or self.current_user["role"] == "admin"
    
    def is_admin(self):
        """Verifica se é administrador"""
        return self.is_authenticated() and self.current_user["role"] == "admin"
    
    def register_user(self, username, password, full_name, email="", role="tecnico"):
        """Registra novo usuário (apenas admin pode criar outros admins)"""
        if role == "admin" and not self.is_admin():
            return False, "Apenas administradores podem criar outros administradores!"
        
        
        
        return self.database.create_user(username, password, full_name, email, role)