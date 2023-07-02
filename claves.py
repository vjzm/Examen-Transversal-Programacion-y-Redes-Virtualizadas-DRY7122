import pyotp
import sqlite3
import hashlib
import uuid
from flask import Flask, request

app = Flask(__name__)

db_name = 'usuarios.db'

def hash_password(password):
    # Generar un hash de la contraseña utilizando hashlib
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

@app.route('/')
def index():
    return 'Sitio web de gestión de claves'

@app.route('/registro/v1', methods=['POST'])
def registro_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (nombre TEXT PRIMARY KEY NOT NULL, 
                contraseña TEXT NOT NULL)''')
    conn.commit()

    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)

    try:
        c.execute("INSERT INTO usuarios (nombre, contraseña) VALUES (?, ?)",
                  (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ya ha sido registrado."

    return "Registro exitoso"

def verificar_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT contraseña FROM usuarios WHERE nombre = ?", (username,))
    records = c.fetchone()
    conn.close()

    if not records:
        return False

    hashed_password = hash_password(password)
    return records[0] == hashed_password

@app.route('/inicio-sesion/v1', methods=['POST'])
def inicio_sesion_v1():
    username = request.form['username']
    password = request.form['password']

    if verificar_hash(username, password):
        return 'Inicio de sesión exitoso'
    else:
        return 'Nombre de usuario o contraseña inválidos'

@app.route('/eliminar-usuario/v1', methods=['POST'])
def eliminar_usuario_v1():
    username = request.form['username']

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE nombre = ?", (username,))
    conn.commit()
    conn.close()

    return "Usuario eliminado exitosamente"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4850)
