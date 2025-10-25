import customtkinter as ctk
from tkinter import ttk, messagebox

class UserManagerWindow:
    def __init__(self, auth_manager, database):
        self.auth_manager = auth_manager
        self.database = database
        self.setup_ui()
    
    def setup_ui(self):
        """Configura interface do gerenciador de usuários"""
        self.window = ctk.CTkToplevel()
        self.window.title("Gerenciar Usuários - MapTopologia")
        self.window.geometry("800x500")
        self.window.minsize(700, 400)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text="Gerenciamento de Usuários",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=10)
        
        # Botão para adicionar usuário
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ Adicionar Usuário",
            command=self.show_add_user_dialog
        )
        add_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Atualizar",
            command=self.load_users
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Lista de usuários
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Usuário", "Nome", "Email", "Função", "Ativo", "Criado em")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        column_widths = [50, 100, 150, 150, 80, 60, 120]
        for col, width in zip(columns, column_widths):
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão duplo clique para editar
        self.users_tree.bind("<Double-1>", self.edit_user)
        
        # Carregar usuários
        self.load_users()
    
    def load_users(self):
        """Carrega lista de usuários"""
        success, users = self.database.get_all_users()
        
        if not success:
            messagebox.showerror("Erro", users)
            return
        
        # Limpar lista
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Adicionar usuários
        for user in users:
            self.users_tree.insert("", "end", values=(
                user['id'],
                user['username'],
                user['full_name'],
                user['email'],
                user['role'],
                "Sim" if user['is_active'] else "Não",
                user['created_at'][:19] if user['created_at'] else ""
            ))
    
    def show_add_user_dialog(self):
        """Mostra diálogo para adicionar usuário"""
        dialog = AddUserDialog(self.window, self.auth_manager, self.database, self)
        dialog.show()
    
    def edit_user(self, event):
        """Edita usuário selecionado"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        user_data = self.users_tree.item(item)['values']
        
        user_id = user_data[0]
        username = user_data[1]
        full_name = user_data[2]
        email = user_data[3]
        role = user_data[4]
        is_active = user_data[5] == "Sim"
        
        dialog = EditUserDialog(
            self.window, self.auth_manager, self.database, self,
            user_id, username, full_name, email, role, is_active
        )
        dialog.show()

class AddUserDialog:
    def __init__(self, parent, auth_manager, database, user_manager):
        self.auth_manager = auth_manager
        self.database = database
        self.user_manager = user_manager
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Adicionar Usuário")
        self.dialog.geometry("400x450")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura interface do diálogo"""
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Novo Usuário", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=10)
        
        # Nome completo
        ctk.CTkLabel(form_frame, text="Nome Completo:*").pack(anchor="w", pady=(10, 0))
        self.full_name_entry = ctk.CTkEntry(form_frame)
        self.full_name_entry.pack(fill="x", pady=(5, 10))
        
        # Usuário
        ctk.CTkLabel(form_frame, text="Nome de Usuário:*").pack(anchor="w")
        self.username_entry = ctk.CTkEntry(form_frame)
        self.username_entry.pack(fill="x", pady=(5, 10))
        
        # Email
        ctk.CTkLabel(form_frame, text="Email:").pack(anchor="w")
        self.email_entry = ctk.CTkEntry(form_frame)
        self.email_entry.pack(fill="x", pady=(5, 10))
        
        # Senha
        ctk.CTkLabel(form_frame, text="Senha:*").pack(anchor="w")
        self.password_entry = ctk.CTkEntry(form_frame, show="•")
        self.password_entry.pack(fill="x", pady=(5, 10))
        
        # Confirmar senha
        ctk.CTkLabel(form_frame, text="Confirmar Senha:*").pack(anchor="w")
        self.confirm_password_entry = ctk.CTkEntry(form_frame, show="•")
        self.confirm_password_entry.pack(fill="x", pady=(5, 10))
        
        # Função
        ctk.CTkLabel(form_frame, text="Função:*").pack(anchor="w")
        self.role_var = ctk.StringVar(value="tecnico")
        
        role_frame = ctk.CTkFrame(form_frame)
        role_frame.pack(fill="x", pady=(5, 10))
        
        ctk.CTkRadioButton(role_frame, text="Técnico", variable=self.role_var, value="tecnico").pack(side="left", padx=10)
        if self.auth_manager.is_admin():
            ctk.CTkRadioButton(role_frame, text="Administrador", variable=self.role_var, value="admin").pack(side="left", padx=10)
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(button_frame, text="Cancelar", command=self.dialog.destroy, fg_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Salvar", command=self.save_user).pack(side="right", padx=5)
        
        self.full_name_entry.focus()
    
    def save_user(self):
        """Salva novo usuário"""
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_var.get()
        
        # Validações
        if not all([full_name, username, password]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Aviso", "As senhas não coincidem!")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres!")
            return
        
        # Criar usuário
        success, message = self.auth_manager.register_user(username, password, full_name, email, role)
        
        if success:
            messagebox.showinfo("Sucesso", message)
            self.dialog.destroy()
            self.user_manager.load_users()
        else:
            messagebox.showerror("Erro", message)
    
    def show(self):
        """Mostra o diálogo"""
        self.dialog.wait_window()

class EditUserDialog(AddUserDialog):
    def __init__(self, parent, auth_manager, database, user_manager, user_id, username, full_name, email, role, is_active):
        self.user_id = user_id
        self.original_username = username
        
        super().__init__(parent, auth_manager, database, user_manager)
        self.dialog.title("Editar Usuário")
        
        # Preencher campos
        self.full_name_entry.delete(0, "end")
        self.full_name_entry.insert(0, full_name)
        
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, username)
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, email)
        
        self.role_var.set(role)
        
        # Remover campos de senha
        for widget in self.dialog.winfo_children():
            if "password" in str(widget).lower():
                widget.pack_forget()
    
    def save_user(self):
        """Atualiza usuário"""
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_var.get()
        
        if not all([full_name, username]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        
        # Atualizar usuário
        success, message = self.database.update_user(
            self.user_id, 
            full_name=full_name,
            email=email,
            role=role
        )
        
        if success:
            messagebox.showinfo("Sucesso", message)
            self.dialog.destroy()
            self.user_manager.load_users()
        else:
            messagebox.showerror("Erro", message)