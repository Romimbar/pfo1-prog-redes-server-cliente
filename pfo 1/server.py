import socket
import sqlite3
import threading
from datetime import datetime


# ==============================
# Función para inicializar DB
# ==============================
def init_db():
    """Crea la base de datos SQLite y la tabla mensajes si no existe."""
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
        exit(1)


# ==============================
# Función para guardar mensaje
# ==============================
def save_message(contenido, ip_cliente):
    """Guarda un mensaje en la base de datos junto con la IP y la fecha."""
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) "
            "VALUES (?, ?, ?)",
            (contenido, fecha, ip_cliente),
        )
        conn.commit()
        conn.close()
        return fecha
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo guardar el mensaje: {e}")
        return None


# ==============================
# Función para inicializar socket
# ==============================
def init_socket():
    """Crea y configura el socket del servidor."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Vincular a localhost:5000
        server_socket.bind(("127.0.0.1", 5000))
        server_socket.listen(5)  # Permite hasta 5 conexiones en espera
        print("[SERVIDOR] Esperando conexiones en 127.0.0.1:5000...")
        return server_socket
    except OSError as e:
        print(f"[ERROR] No se pudo iniciar el socket: {e}")
        exit(1)


# ==============================
# Función para manejar clientes
# ==============================
def handle_client(conn, addr):
    """Maneja la comunicación con un cliente específico."""
    print(f"[NUEVA CONEXIÓN] Cliente conectado desde {addr}")
    while True:
        try:
            data = conn.recv(1024).decode("utf-8")  # Recibe hasta 1024 bytes
            if not data:
                break

            print(f"[MENSAJE] {addr}: {data}")

            # Guardar mensaje en la DB
            fecha = save_message(data, addr[0])
            if fecha:
                respuesta = f"Mensaje recibido: {fecha}"
            else:
                respuesta = "Error al guardar mensaje."

            conn.send(respuesta.encode("utf-8"))

        except Exception as e:
            print(f"[ERROR] Problema con el cliente {addr}: {e}")
            break
    conn.close()
    print(f"[DESCONECTADO] Cliente {addr} se desconectó.")


# ==============================
# Programa principal (Servidor)
# ==============================
if __name__ == "__main__":
    init_db()
    server_socket = init_socket()

    while True:
        conn, addr = server_socket.accept()
        # Crear un hilo para cada cliente
        hilo = threading.Thread(target=handle_client, args=(conn, addr))
        hilo.start()
        print(f"[ACTIVOS] Clientes atendidos en paralelo: "
              f"{threading.active_count() - 1}")
