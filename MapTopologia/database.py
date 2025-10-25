import sqlite3
import json
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self):
        self.db_file = "network_map.db"
        self.init_database()
    
    def init_database(self):
        """Inicializa banco de dados com todas as tabelas"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    role TEXT DEFAULT 'tecnico',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de dispositivos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT UNIQUE,
                    mac TEXT,
                    hostname TEXT,
                    vendor TEXT,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Tabela de scans
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    network_range TEXT,
                    devices_found INTEGER,
                    scan_date TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabela de topologias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS topologies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    devices_data TEXT,
                    created_at TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Inserir usuário admin padrão se não existir
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                admin_password = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', admin_password, 'Administrador', 'admin@empresa.com', 'admin'))
            
            # Inserir usuário técnico padrão
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'tecnico'")
            if cursor.fetchone()[0] == 0:
                tecnico_password = hashlib.sha256("tec123".encode()).hexdigest()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('tecnico', tecnico_password, 'Técnico de Rede', 'tecnico@empresa.com', 'tecnico'))
            
            conn.commit()
            conn.close()
            print("Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
    
    # ========== MÉTODOS DE AUTENTICAÇÃO ==========
    
    def authenticate_user(self, username, password):
        """Autentica usuário no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                SELECT id, username, full_name, email, role, is_active 
                FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'full_name': user[2],
                    'email': user[3],
                    'role': user[4],
                    'is_active': bool(user[5])
                }
            return None
            
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None
    
    def create_user(self, username, password, full_name, email="", role="tecnico"):
        """Cria novo usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Verificar se usuário já existe
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return False, "Usuário já existe!"
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, full_name, email, role))
            
            conn.commit()
            conn.close()
            return True, "Usuário criado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao criar usuário: {e}"
    
    def get_all_users(self):
        """Recupera todos os usuários (apenas para admin)"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, full_name, email, role, created_at, is_active
                FROM users 
                ORDER BY created_at DESC
            ''')
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'email': row[3],
                    'role': row[4],
                    'created_at': row[5],
                    'is_active': bool(row[6])
                })
            
            conn.close()
            return True, users
            
        except Exception as e:
            return False, f"Erro ao recuperar usuários: {e}"
    
    def update_user(self, user_id, full_name=None, email=None, role=None, is_active=None):
        """Atualiza informações do usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if full_name is not None:
                updates.append("full_name = ?")
                params.append(full_name)
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            if role is not None:
                updates.append("role = ?")
                params.append(role)
            if is_active is not None:
                updates.append("is_active = ?")
                params.append(1 if is_active else 0)
            
            if updates:
                params.append(user_id)
                cursor.execute(f'''
                    UPDATE users 
                    SET {', '.join(updates)} 
                    WHERE id = ?
                ''', params)
                
                conn.commit()
            
            conn.close()
            return True, "Usuário atualizado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao atualizar usuário: {e}"
    
    # ========== MÉTODOS DE REDE ==========
    
    def save_scan_results(self, devices, network_range, user_id=None):
        """Salva resultados do scan"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            timestamp = datetime.now()
            
            # Salva scan
            cursor.execute(
                "INSERT INTO scans (network_range, devices_found, scan_date, user_id) VALUES (?, ?, ?, ?)",
                (network_range, len(devices), timestamp, user_id)
            )
            
            # Atualiza dispositivos
            for device in devices:
                cursor.execute('''
                    INSERT OR REPLACE INTO devices 
                    (ip, mac, hostname, vendor, first_seen, last_seen, created_by)
                    VALUES (?, ?, ?, ?, COALESCE((SELECT first_seen FROM devices WHERE ip = ?), ?), ?, ?)
                ''', (
                    device['ip'], device['mac'], device['hostname'], device['vendor'],
                    device['ip'], timestamp, timestamp, user_id
                ))
            
            conn.commit()
            conn.close()
            return True, "Scan salvo com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao salvar scan: {e}"
    
    def get_scan_history(self, limit=10, user_id=None):
        """Recupera histórico de scans"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT s.id, s.network_range, s.devices_found, s.scan_date, u.username
                    FROM scans s
                    LEFT JOIN users u ON s.user_id = u.id
                    WHERE s.user_id = ?
                    ORDER BY s.scan_date DESC 
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor.execute('''
                    SELECT s.id, s.network_range, s.devices_found, s.scan_date, u.username
                    FROM scans s
                    LEFT JOIN users u ON s.user_id = u.id
                    ORDER BY s.scan_date DESC 
                    LIMIT ?
                ''', (limit,))
            
            scans = []
            for row in cursor.fetchall():
                scans.append({
                    'id': row[0],
                    'network_range': row[1],
                    'devices_found': row[2],
                    'scan_date': row[3],
                    'username': row[4] or 'Sistema'
                })
            
            conn.close()
            return True, scans
            
        except Exception as e:
            return False, f"Erro ao recuperar histórico: {e}"
    
    def get_all_devices(self):
        """Recupera todos os dispositivos"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT ip, mac, hostname, vendor, last_seen 
                FROM devices 
                ORDER BY last_seen DESC
            ''')
            
            devices = []
            for row in cursor.fetchall():
                devices.append({
                    'ip': row[0],
                    'mac': row[1],
                    'hostname': row[2],
                    'vendor': row[3],
                    'last_seen': row[4],
                    'status': 'Online'
                })
            
            conn.close()
            return True, devices
            
        except Exception as e:
            return False, f"Erro ao recuperar dispositivos: {e}"
    
    def get_user_stats(self, user_id):
        """Recupera estatísticas do usuário"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Total de scans
            cursor.execute("SELECT COUNT(*) FROM scans WHERE user_id = ?", (user_id,))
            total_scans = cursor.fetchone()[0]
            
            # Total de dispositivos encontrados
            cursor.execute('''
                SELECT COUNT(DISTINCT ip) FROM devices WHERE created_by = ?
            ''', (user_id,))
            total_devices = cursor.fetchone()[0]
            
            # Último scan
            cursor.execute('''
                SELECT scan_date FROM scans 
                WHERE user_id = ? 
                ORDER BY scan_date DESC LIMIT 1
            ''', (user_id,))
            last_scan = cursor.fetchone()
            
            conn.close()
            
            return {
                'total_scans': total_scans,
                'total_devices': total_devices,
                'last_scan': last_scan[0] if last_scan else None
            }
            
        except Exception as e:
            print(f"Erro ao recuperar estatísticas: {e}")
            return {}