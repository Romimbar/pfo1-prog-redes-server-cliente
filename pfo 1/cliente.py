import socket


# ==============================
# Configuración del cliente
# ==============================
def init_client():
    """Crea y configura el socket del cliente para conectarse al servidor."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 5000))
        # Conexión al servidor en localhost:5000
        print("[CLIENTE] Conectado al servidor en 127.0.0.1:5000")
        return client_socket
    except OSError as e:
        print(f"[ERROR] No se pudo conectar al servidor: {e}")
        exit(1)


# ==============================
# Función principal del cliente
# ==============================
def run_client():
    """Permite enviar mensajes al servidor hasta escribir 'éxito'."""
    client_socket = init_client()

    while True:
        mensaje = input("Escribí tu mensaje ('éxito' para salir): ")

        if mensaje.lower() == "éxito":
            print("[CLIENTE] Cerrando conexión...")
            break

        try:
            # Enviar mensaje al servidor
            client_socket.send(mensaje.encode("utf-8"))

            # Esperar respuesta del servidor
            respuesta = client_socket.recv(1024).decode("utf-8")
            print(f"[SERVIDOR] {respuesta}")

        except Exception as e:
            print(f"[ERROR] No se pudo enviar/recibir mensaje: {e}")
            break

    client_socket.close()


# ==============================
# Programa principal (Cliente)
# ==============================
if __name__ == "__main__":
    run_client()
