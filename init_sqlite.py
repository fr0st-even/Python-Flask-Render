import sqlite3
import os
import bcrypt
import datetime

# Ruta donde se guardara la base de datos
db_path = './data/users.db'

# Crea la carpeta si no existe
os.makedirs('./data', exist_ok=True)

# Conexion a sqlite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Creacion de tabla usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        profile_photo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) 
''')

# Creacion de tabla imagenes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        filedata TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Creacion de tabla comentarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (image_id) REFERENCES images (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Creacion de tabla likes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(image_id, user_id),
        FOREIGN KEY (image_id) REFERENCES images (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Verificar columnas existentes en users
cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]

# Agregar columnas si no existen
if 'profile_photo' not in columns:
    cursor.execute('ALTER TABLE users ADD COLUMN profile_photo TEXT')

if 'created_at' not in columns:
    cursor.execute('ALTER TABLE users ADD COLUMN created_at TIMESTAMP')

# Usuarios Iniciales
init_users = [
    ('Iosef', '1234'), # id: 1
]

# Verificar si ya existen usuarios
cursor.execute('SELECT COUNT(*) FROM users')
user_count = cursor.fetchone()[0]

# Solo insertar usuarios iniciales si la tabla está vacía
if user_count == 0:
    print("Insertando usuarios iniciales...")
    for username, password in init_users:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        created_at = datetime.datetime.now()
        cursor.execute('''
            INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)
        ''', (username, hashed_password.decode('utf-8'), created_at))
    print("Usuarios iniciales insertados correctamente")
else:
    print(f"Ya existen {user_count} usuarios en la base de datos")

# Guardar y cerrar conexión
conn.commit()
conn.close()

print("Base de datos y tablas creadas/actualizadas correctamente")