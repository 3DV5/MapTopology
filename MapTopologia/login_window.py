import customtkinter as ctk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, auth_manager, on_login_success, on_register_click):
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        self.on_register_click = on_register_click
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura interface de login idêntica ao anexo"""
        self.window = ctk.CTkToplevel()
        self.window.title("MapTopologia - Login")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.transient()
        self.window.grab_set()
        
        # Configurar tema claro
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Centralizar na tela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"400x500+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(
            self.window, 
            fg_color="white",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Espaço superior
        ctk.CTkFrame(main_frame, height=60, fg_color="white").pack()
        
        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text="Login",
            font=ctk.CTkFont(size=32, weight="bold", family="Arial"),
            text_color="black"
        )
        title.pack(pady=(0, 40))
        
        # Formulário
        form_frame = ctk.CTkFrame(main_frame, fg_color="white")
        form_frame.pack(fill="x", padx=50, pady=0)
        
        # Campo de usuário
        user_label = ctk.CTkLabel(
            form_frame, 
            text="Usuário",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="black",
            anchor="w"
        )
        user_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=1,
            corner_radius=8,
            fg_color="white",
            text_color="black",
            border_color="#CCCCCC"
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        
        # Campo de senha
        password_label = ctk.CTkLabel(
            form_frame, 
            text="Senha",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="black",
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=1,
            corner_radius=8,
            fg_color="white",
            text_color="black",
            border_color="#CCCCCC",
            show="•"
        )
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        # Link "Esqueceu sua senha?"
        forgot_password = ctk.CTkLabel(
            form_frame,
            text="Esqueceu sua senha? clique aqui",
            font=ctk.CTkFont(size=12),
            text_color="#0066CC",
            cursor="hand2"
        )
        forgot_password.pack(anchor="e", pady=(0, 30))
        forgot_password.bind("<Button-1>", lambda e: self.forgot_password())
        
        # Botão Entrar
        self.login_btn = ctk.CTkButton(
            form_frame,
            text="Entrar",
            command=self.login,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            corner_radius=8,
            border_width=0,
            text_color="white"
        )
        self.login_btn.pack(fill="x", pady=(0, 30))
        
        # Link "criar uma conta"
        register_link = ctk.CTkLabel(
            form_frame,
            text="criar uma conta",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="#0066CC",
            cursor="hand2"
        )
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.show_register())
        
        # Credenciais de teste (apenas para desenvolvimento)
        if __debug__:
            test_frame = ctk.CTkFrame(main_frame, fg_color="white")
            test_frame.pack(side="bottom", fill="x", pady=20)
            
            test_label = ctk.CTkLabel(
                test_frame,
                text="💡 Teste: admin/admin123 | tecnico/tec123",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            test_label.pack()
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Focar no campo de usuário
        self.username_entry.focus()
    
    def login(self):
        """Processa tentativa de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        self.login_btn.configure(
            state="disabled", 
            text="Entrando...",
            fg_color="gray"
        )
        
        # Processar login
        self.window.after(100, self._process_login, username, password)
    
    def _process_login(self, username, password):
        """Processa login em segundo plano"""
        success, message = self.auth_manager.login(username, password)
        
        if success:
            self.window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Erro de Login", message)
            self.login_btn.configure(
                state="normal", 
                text="Entrar",
                fg_color="#0066CC"
            )
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
    
    def forgot_password(self):
        """Função para esqueci senha"""
        messagebox.showinfo("Recuperar Senha", 
                           "Entre em contato com o administrador do sistema para redefinir sua senha.")
    
    def show_register(self):
        """Mostra tela de cadastro"""
        self.window.destroy()
        self.on_register_click()
    
    def show(self):
        """Mostra a janela de login"""
        self.window.wait_window()