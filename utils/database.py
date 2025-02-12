import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

class DatabaseManager:
    def __init__(self):
        # Crear directorio data si no existe
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Ruta completa de la base de datos
        self.db_path = os.path.join(self.data_dir, 'users.db')

    def get_db_connection(self):
        """Obtiene conexión a la base de datos"""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Inicializa la base de datos y crea la tabla de usuarios"""
        with self.get_db_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    name TEXT,
                    email TEXT
                )
            ''')
            conn.commit()

    def add_user(self, username, password, role='user', name='', email=''):
        """Agrega un nuevo usuario a la base de datos"""
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor()
                hashed_password = generate_password_hash(password)
                c.execute(
                    "INSERT INTO users (username, password, role, name, email) VALUES (?, ?, ?, ?, ?)",
                    (username, hashed_password, role, name, email)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        """Valida las credenciales del usuario"""
        with self.get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT password, role, name, email FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            
            if result and check_password_hash(result[0], password):
                return {
                    "username": username,
                    "role": result[1],
                    "name": result[2],
                    "email": result[3]
                }
            return None

    def get_user(self, username):
        """Obtiene información del usuario"""
        with self.get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT role, name, email FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            
            if result:
                return {
                    "username": username,
                    "role": result[0],
                    "name": result[1],
                    "email": result[2]
                }
            return None

    def update_user(self, username, data):
        """Actualiza información del usuario"""
        with self.get_db_connection() as conn:
            c = conn.cursor()
            updates = []
            values = []
            for key, value in data.items():
                if key != 'username':
                    if key == 'password':
                        value = generate_password_hash(value)
                    updates.append(f"{key} = ?")
                    values.append(value)
            
            if updates:
                values.append(username)
                query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
                c.execute(query, values)
                conn.commit()
                return True
            return False