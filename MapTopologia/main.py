import customtkinter as ctk
from tkinter import ttk, messagebox
import threading
import os
from datetime import datetime
from config import Config
from network_scanner import NetworkScanner
from topology_builder import TopologyBuilder
from pdf_exporter import PDFExporter
from auth_manager import AuthManager
from database import DatabaseManager
from login_window import LoginWindow
from register_window import RegisterWindow
from user_manager import UserManagerWindow

class MapTopologiaApp:
    def __init__(self):
        # Configuração inicial
        Config.setup_directories()
        
        # Inicializar componentes
        self.database = DatabaseManager()
        self.auth_manager = AuthManager(self.database)
        self.scanner = NetworkScanner()
        self.topology_builder = TopologyBuilder()
        self.pdf_exporter = PDFExporter()
        
        # Dados atuais
        self.current_devices = []
        self.current_topology_image = None
        
        # Configurar interface
        self.setup_ui()
        
        # Mostrar login inicial
        self.show_login()
        
    def setup_ui(self):
        """Configura interface do usuário"""
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title(f"{Config.APP_NAME} v{Config.VERSION}")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Criar layout principal (inicialmente escondido)
        self.create_main_layout()
        
    def create_main_layout(self):
        """Cria layout principal da aplicação"""
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white")
        # Não pack ainda - será mostrado após login
        
    def create_authenticated_ui(self):
        """Cria interface após autenticação"""
        # Empacotar frame principal
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra lateral
        self.create_sidebar(self.main_frame)
        
        # Área de conteúdo
        self.create_content_area(self.main_frame)
        
        # Mostrar aba inicial
        self.show_scan_tab()
    
    def create_sidebar(self, parent):
        """Cria barra lateral com navegação"""
        sidebar = ctk.CTkFrame(parent, width=220, fg_color="#f8f9fa")
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            sidebar, 
            text="MapTopologia",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="black"
        )
        title_label.pack(pady=30)
        
        # Botões de navegação
        nav_buttons = [
            ("🔍 Varredura de Rede", self.show_scan_tab),
            ("🌐 Topologia", self.show_topology_tab),
            ("📊 Relatórios", self.show_reports_tab),
        ]
        
        # Adicionar gerenciamento de usuários se for admin
        if self.auth_manager.is_admin():
            nav_buttons.append(("👥 Gerenciar Usuários", self.show_user_management))
        
        nav_buttons.append(("⚙️ Configurações", self.show_settings_tab))
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                anchor="w",
                height=45,
                fg_color="transparent",
                hover_color="#e9ecef",
                text_color="black",
                font=ctk.CTkFont(size=14)
            )
            btn.pack(fill="x", padx=15, pady=8)
        
        # Espaço flexível
        ctk.CTkFrame(sidebar, height=1, fg_color="#f8f9fa").pack(fill="x", pady=20)
        
        # Status do usuário
        status_frame = ctk.CTkFrame(sidebar, fg_color="#f8f9fa")
        status_frame.pack(side="bottom", fill="x", padx=10, pady=15)
        
        user_info = self.auth_manager.get_current_user()
        if user_info:
            user_text = f"👤 {user_info['full_name']}"
            role_text = f"({user_info['role'].capitalize()})"
            
            user_label = ctk.CTkLabel(status_frame, text=user_text, 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color="black")
            user_label.pack(pady=(10, 0))
            
            role_label = ctk.CTkLabel(status_frame, text=role_text, 
                                    font=ctk.CTkFont(size=10), 
                                    text_color="gray")
            role_label.pack(pady=(0, 10))
        
        # Botão logout
        logout_btn = ctk.CTkButton(
            status_frame,
            text="🚪 Sair",
            command=self.logout,
            height=35,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        logout_btn.pack(fill="x", pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(status_frame, text="Sistema pronto", 
                                       text_color="green", font=ctk.CTkFont(size=10))
        self.status_label.pack(pady=5)
        
    def create_content_area(self, parent):
        """Cria área de conteúdo principal"""
        self.content_area = ctk.CTkFrame(parent, fg_color="white")
        self.content_area.pack(fill="both", expand=True)
    
    def show_scan_tab(self):
        """Mostra aba de varredura de rede"""
        self.clear_content_area()
        
        # Título
        title = ctk.CTkLabel(self.content_area, text="🔍 Varredura de Rede", 
                           font=ctk.CTkFont(size=24, weight="bold"),
                           text_color="black")
        title.pack(pady=20)
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        controls_frame.pack(fill="x", padx=30, pady=15)
        
        # Grid para controles
        controls_frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(controls_frame, text="Faixa de Rede:", 
                    font=ctk.CTkFont(size=14),
                    text_color="black").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.network_entry = ctk.CTkEntry(
            controls_frame, 
            width=300, 
            font=ctk.CTkFont(size=13), 
            height=35,
            fg_color="white",
            text_color="black",
            border_color="#CCCCCC"
        )
        self.network_entry.insert(0, Config.DEFAULT_NETWORK_RANGE)
        self.network_entry.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        
        self.scan_btn = ctk.CTkButton(
            controls_frame, 
            text="Iniciar Varredura", 
            command=self.start_scan,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            text_color="white"
        )
        self.scan_btn.grid(row=0, column=2, padx=15, pady=15)
        
        # Frame de resultados
        results_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        results_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Título dos resultados
        results_title = ctk.CTkLabel(results_frame, text="Dispositivos Encontrados", 
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   text_color="black")
        results_title.pack(pady=10)
        
        # Treeview para dispositivos
        columns = ("IP", "MAC", "Hostname", "Fabricante", "Status")
        self.devices_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        column_widths = [150, 180, 200, 150, 100]
        for col, width in zip(columns, column_widths):
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=width, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.devices_tree.yview)
        self.devices_tree.configure(yscrollcommand=scrollbar.set)
        
        self.devices_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def show_topology_tab(self):
        """Mostra aba de topologia"""
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text="🌐 Topologia de Rede", 
                           font=ctk.CTkFont(size=24, weight="bold"),
                           text_color="black")
        title.pack(pady=20)
        
        # Controles
        controls_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        controls_frame.pack(fill="x", padx=30, pady=15)
        
        self.generate_topology_btn = ctk.CTkButton(
            controls_frame,
            text="Gerar Topologia Visual",
            command=self.generate_topology,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            text_color="white"
        )
        self.generate_topology_btn.pack(side="left", padx=10, pady=10)
        
        # Info label
        info_label = ctk.CTkLabel(controls_frame, 
                                text="Execute uma varredura primeiro para gerar a topologia",
                                font=ctk.CTkFont(size=12),
                                text_color="gray")
        info_label.pack(side="left", padx=20, pady=10)
        
        # Área da topologia
        topology_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        topology_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        self.topology_label = ctk.CTkLabel(
            topology_frame, 
            text="A topologia será exibida aqui após a geração\n\nExecute uma varredura e clique em 'Gerar Topologia Visual'",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.topology_label.pack(expand=True)
        
        # Se já temos uma imagem, mostra ela
        if self.current_topology_image:
            self.topology_label.configure(image=self.current_topology_image, text="")
    
    def show_reports_tab(self):
        """Mostra aba de relatórios"""
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text="📊 Relatórios", 
                           font=ctk.CTkFont(size=24, weight="bold"),
                           text_color="black")
        title.pack(pady=20)
        
        # Controles
        controls_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        controls_frame.pack(fill="x", padx=30, pady=15)
        
        self.export_pdf_btn = ctk.CTkButton(
            controls_frame,
            text="📄 Exportar Relatório PDF",
            command=self.export_pdf_report,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            text_color="white"
        )
        self.export_pdf_btn.pack(side="left", padx=10, pady=10)
        
        # Info label
        info_label = ctk.CTkLabel(controls_frame, 
                                text="Gere um relatório completo em PDF com os dados da rede",
                                font=ctk.CTkFont(size=12),
                                text_color="gray")
        info_label.pack(side="left", padx=20, pady=10)
        
        # Área de informações
        info_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        info_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        info_title = ctk.CTkLabel(info_frame, text="Informações do Relatório", 
                                font=ctk.CTkFont(size=16, weight="bold"),
                                text_color="black")
        info_title.pack(pady=10)
        
        self.report_info = ctk.CTkTextbox(
            info_frame, 
            font=ctk.CTkFont(size=12), 
            height=20,
            fg_color="white",
            text_color="black",
            border_color="#CCCCCC"
        )
        self.report_info.pack(fill="both", expand=True, padx=10, pady=10)
        self.report_info.insert("1.0", 
            "Relatório de Topologia de Rede - MapTopologia\n\n"
            "Execute uma varredura de rede primeiro para gerar relatórios.\n\n"
            "O relatório PDF incluirá:\n"
            "• Lista completa de dispositivos de rede\n"
            "• Informações técnicas (IP, MAC, Hostname)\n"
            "• Fabricante dos equipamentos\n"
            "• Status dos dispositivos\n"
            "• Metadados da varredura\n\n"
            "Clique em 'Exportar Relatório PDF' para gerar o documento."
        )
    
    def show_settings_tab(self):
        """Mostra aba de configurações"""
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text="⚙️ Configurações", 
                           font=ctk.CTkFont(size=24, weight="bold"),
                           text_color="black")
        title.pack(pady=20)
        
        # Configurações de rede
        network_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        network_frame.pack(fill="x", padx=30, pady=15)
        
        ctk.CTkLabel(network_frame, text="Configurações de Rede", 
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color="black").pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(network_frame, text="Faixa de Rede Padrão:", 
                    font=ctk.CTkFont(size=14),
                    text_color="black").pack(anchor="w", padx=15, pady=(10, 5))
        
        self.default_network_entry = ctk.CTkEntry(
            network_frame, 
            height=35, 
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="black",
            border_color="#CCCCCC"
        )
        self.default_network_entry.insert(0, Config.DEFAULT_NETWORK_RANGE)
        self.default_network_entry.pack(fill="x", padx=15, pady=(5, 15))
        
        # Botão para aplicar configurações
        apply_btn = ctk.CTkButton(
            network_frame,
            text="💾 Aplicar Configurações",
            command=self.apply_settings,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#0066CC",
            hover_color="#0052A3",
            text_color="white"
        )
        apply_btn.pack(padx=15, pady=15)
    
    def clear_content_area(self):
        """Limpa a área de conteúdo"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Mostra janela de login"""
        login_window = LoginWindow(
            self.auth_manager, 
            self.on_login_success, 
            self.show_register
        )
        login_window.show()
    
    def show_register(self):
        """Mostra janela de cadastro"""
        register_window = RegisterWindow(
            self.auth_manager,
            self.database,
            self.show_login,
            self.on_register_success
        )
        register_window.show()
    
    def on_login_success(self):
        """Callback quando login é bem-sucedido"""
        # Criar interface autenticada
        self.create_authenticated_ui()
        
        # Mostrar mensagem de boas-vindas
        user_info = self.auth_manager.get_current_user()
        messagebox.showinfo("Bem-vindo", f"Login realizado com sucesso!\n\nBem-vindo, {user_info['full_name']}!")
    
    def on_register_success(self):
        """Callback quando cadastro é bem-sucedido"""
        # Se um admin criou um usuário, apenas mostra mensagem
        if self.auth_manager.is_authenticated():
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        else:
            # Se foi cadastro público, volta para login
            messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça login para continuar.")
            self.show_login()
    
    def logout(self):
        """Realiza logout"""
        success, message = self.auth_manager.logout()
        if success:
            # Destruir interface atual
            self.main_frame.destroy()
            
            # Recriar frame principal
            self.create_main_layout()
            
            # Limpar dados
            self.current_devices = []
            self.current_topology_image = None
            
            # Mostrar login novamente
            self.show_login()
    
    def show_user_management(self):
        """Mostra gerenciamento de usuários"""
        if not self.auth_manager.is_admin():
            messagebox.showwarning("Aviso", "Apenas administradores podem acessar esta funcionalidade!")
            return
        
        UserManagerWindow(self.auth_manager, self.database)
    
    def start_scan(self):
        """Inicia varredura de rede em thread separada"""
        network_range = self.network_entry.get().strip()
        if not network_range:
            messagebox.showwarning("Aviso", "Digite uma faixa de rede válida!")
            return
        
        self.scan_btn.configure(state="disabled", text="Varrendo Rede...")
        self.status_label.configure(text="Varredura em andamento...", text_color="orange")
        
        def scan_thread():
            devices = self.scanner.arp_scan(network_range)
            self.root.after(0, self.scan_completed, devices, network_range)
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def scan_completed(self, devices, network_range):
        """Callback quando varredura é completada"""
        self.scan_btn.configure(state="normal", text="Iniciar Varredura")
        
        if isinstance(devices, dict) and "error" in devices:
            messagebox.showerror("Erro", devices["error"])
            self.status_label.configure(text="Erro na varredura", text_color="red")
            return
        
        # Atualiza dispositivos atuais
        self.current_devices = devices
        
        # Atualiza treeview
        self.devices_tree.delete(*self.devices_tree.get_children())
        
        for device in devices:
            self.devices_tree.insert("", "end", values=(
                device['ip'],
                device['mac'],
                device['hostname'],
                device['vendor'],
                device['status']
            ))
        
        # Salva no banco
        user_info = self.auth_manager.get_current_user()
        user_id = user_info['id'] if user_info else None
        
        success, message = self.database.save_scan_results(devices, network_range, user_id)
        
        if success:
            self.status_label.configure(text=f"Varredura concluída: {len(devices)} dispositivos", text_color="green")
            messagebox.showinfo("Sucesso", f"Varredura concluída!\n{len(devices)} dispositivos encontrados.")
        else:
            self.status_label.configure(text="Varredura concluída (erro no BD)", text_color="orange")
            messagebox.showwarning("Aviso", f"Varredura concluída mas {message}")
    
    def generate_topology(self):
        """Gera topologia visual da rede"""
        if not self.current_devices:
            messagebox.showwarning("Aviso", "Execute uma varredura primeiro para gerar a topologia!")
            return
        
        self.generate_topology_btn.configure(state="disabled", text="Gerando...")
        self.status_label.configure(text="Gerando topologia...", text_color="orange")
        
        def topology_thread():
            try:
                topology_image = self.topology_builder.build_topology(self.current_devices)
                self.root.after(0, self.topology_completed, topology_image)
            except Exception as e:
                print(f"Erro na thread de topologia: {e}")
                # Tenta método alternativo
                try:
                    from PIL import ImageDraw, ImageFont
                    topology_image = self.topology_builder.build_simple_topology(self.current_devices)
                    self.root.after(0, self.topology_completed, topology_image)
                except:
                    self.root.after(0, self.topology_completed, None)
        
        threading.Thread(target=topology_thread, daemon=True).start()
    
    def topology_completed(self, topology_image):
        """Callback quando topologia é gerada"""
        self.generate_topology_btn.configure(state="normal", text="Gerar Topologia Visual")
        
        if topology_image:
            self.current_topology_image = topology_image
            self.topology_label.configure(image=topology_image, text="")
            self.topology_label.image = topology_image  # Manter referência
            self.status_label.configure(text="Topologia gerada com sucesso", text_color="green")
        else:
            self.status_label.configure(text="Erro ao gerar topologia", text_color="red")
            messagebox.showerror("Erro", "Não foi possível gerar a topologia")
    
    def export_pdf_report(self):
        """Exporta relatório PDF"""
        if not self.current_devices:
            messagebox.showwarning("Aviso", "Execute uma varredura primeiro para gerar relatórios!")
            return
        
        self.export_pdf_btn.configure(state="disabled", text="Gerando PDF...")
        self.status_label.configure(text="Gerando relatório PDF...", text_color="orange")
        
        def pdf_thread():
            user_info = self.auth_manager.get_current_user()
            company_name = f"Relatório gerado por: {user_info['full_name']}" if user_info else ""
            
            pdf_path = self.pdf_exporter.export_topology_report(
                self.current_devices,
                company_name
            )
            self.root.after(0, self.pdf_export_completed, pdf_path)
        
        threading.Thread(target=pdf_thread, daemon=True).start()
    
    def pdf_export_completed(self, pdf_path):
        """Callback quando PDF é exportado"""
        self.export_pdf_btn.configure(state="normal", text="📄 Exportar Relatório PDF")
        
        if pdf_path:
            self.status_label.configure(text=f"PDF gerado: {os.path.basename(pdf_path)}", text_color="green")
            
            # Atualiza informações do relatório
            report_text = f"""RELATÓRIO GERADO COM SUCESSO

Arquivo: {pdf_path}
Data: {self.get_current_timestamp()}
Dispositivos encontrados: {len(self.current_devices)}

CONTEÚDO INCLUÍDO:
• Lista completa de dispositivos de rede
• Informações técnicas (IP, MAC, Hostname)
• Fabricante dos equipamentos
• Status dos dispositivos
• Metadados da varredura

O relatório foi salvo na pasta 'reports/'"""
            
            self.report_info.delete("1.0", "end")
            self.report_info.insert("1.0", report_text)
            
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n\nArquivo: {pdf_path}")
        else:
            self.status_label.configure(text="Erro ao gerar PDF", text_color="red")
            messagebox.showerror("Erro", "Falha ao gerar relatório PDF")
    
    def apply_settings(self):
        """Aplica configurações alteradas"""
        new_network_range = self.default_network_entry.get().strip()
        if new_network_range:
            Config.DEFAULT_NETWORK_RANGE = new_network_range
            self.network_entry.delete(0, "end")
            self.network_entry.insert(0, new_network_range)
            messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!")
            self.status_label.configure(text="Configurações atualizadas", text_color="green")
        else:
            messagebox.showwarning("Aviso", "Digite uma faixa de rede válida!")
    
    def get_current_timestamp(self):
        """Retorna timestamp atual formatado"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

# Ponto de entrada
if __name__ == "__main__":
    app = MapTopologiaApp()
    app.run()