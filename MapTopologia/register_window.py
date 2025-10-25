import customtkinter as ctk
from tkinter import messagebox

class RegisterWindow:
    def __init__(self, auth_manager, database, on_back_to_login, on_register_success):
        self.auth_manager = auth_manager
        self.database = database
        self.on_back_to_login = on_back_to_login
        self.on_register_success = on_register_success
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura interface de cadastro idêntica ao anexo"""
        self.window = ctk.CTkToplevel()
        self.window.title("MapTopologia - Criar Conta")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        self.window.transient()
        self.window.grab_set()
        
        # Configurar tema claro
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Centralizar na tela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"400x600+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(
            self.window, 
            fg_color="white",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Espaço superior
        ctk.CTkFrame(main_frame, height=40, fg_color="white").pack()
        
        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text="Criar Conta",
            font=ctk.CTkFont(size=32, weight="bold", family="Arial"),
            text_color="black"
        )
        title.pack(pady=(0, 30))
        
        # Formulário
        form_frame = ctk.CTkFrame(main_frame, fg_color="white")
        form_frame.pack(fill="x", padx=50, pady=0)
        
        # CAMPO USUÁRIO
        user_label = ctk.CTkLabel(
            form_frame, 
            text="Usuario",
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
        
        # CAMPO E-MAIL
        email_label = ctk.CTkLabel(
            form_frame, 
            text="E-mail",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="black",
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
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
        self.email_entry.pack(fill="x", pady=(0, 20))
        
        # CAMPO SENHA
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
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        # CAMPO REPETIR SENHA
        confirm_label = ctk.CTkLabel(
            form_frame, 
            text="Repita sua Senha",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="black",
            anchor="w"
        )
        confirm_label.pack(fill="x", pady=(0, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
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
        self.confirm_password_entry.pack(fill="x", pady=(0, 30))
        
        # Botão Criar
        self.register_btn = ctk.CTkButton(
            form_frame,
            text="Criar",
            command=self.register,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            corner_radius=8,
            border_width=0,
            text_color="white"
        )
        self.register_btn.pack(fill="x", pady=(0, 20))
        
        # Link "Voltar para login"
        login_link = ctk.CTkLabel(
            form_frame,
            text="← Voltar para login",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="#0066CC",
            cursor="hand2"
        )
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.back_to_login())
        
        # Bind Enter key para navegação
        self.username_entry.bind("<Return>", lambda e: self.email_entry.focus())
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.confirm_password_entry.focus())
        self.confirm_password_entry.bind("<Return>", lambda e: self.register())
        
        # Focar no primeiro campo
        self.username_entry.focus()
    
    def register(self):
        """Processa cadastro de novo usuário"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validações
        if not all([username, email, password, confirm_password]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Aviso", "As senhas não coincidem!")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
            self.password_entry.focus()
            return
        
        if len(password) < 4:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres!")
            return
        
        if "@" not in email or "." not in email:
            messagebox.showwarning("Aviso", "Digite um email válido!")
            return
        
        self.register_btn.configure(
            state="disabled", 
            text="Criando...",
            fg_color="gray"
        )
        
        # Processar cadastro
        self.window.after(100, self._process_register, username, password, email)
    
    def _process_register(self, username, password, email):
        """Processa cadastro em segundo plano"""
        # Para cadastro público, sempre cria como técnico
        role = "tecnico"
        full_name = username
        
        success, message = self.auth_manager.register_user(
            username, password, full_name, email, role
        )
        
        if success:
            messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça login para continuar.")
            self.window.destroy()
            self.on_back_to_login()
        else:
            messagebox.showerror("Erro no Cadastro", message)
            self.register_btn.configure(
                state="normal", 
                text="Criar",
                fg_color="#0066CC"
            )
    
    def back_to_login(self):
        """Volta para a tela de login"""
        self.window.destroy()
        self.on_back_to_login()
    
    def show(self):
        """Mostra a janela de cadastro"""
        self.window.wait_window()