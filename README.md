# Chat Cliente-Servidor con Sockets y SQLite

Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos**  
Materia: Programación sobre Redes – IFTS 29  

---
Objetivo
Aprender a configurar un servidor de sockets en Python que reciba mensajes de clientes, los almacene en una base de datos SQLite y envíe confirmaciones.

---
Tecnologías
- Python 3
- Módulos estándar: `socket`, `sqlite3`, `threading`, `datetime`

---
Archivos
- `server.py` → servidor (escucha en `127.0.0.1:5000`)
- `cliente.py` → cliente (se conecta y envía mensajes)
- `chat.db` → base de datos SQLite (se genera automáticamente al ejecutar el servidor)

---
Ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/USUARIO/chat-sockets-python.git
   cd chat-sockets-python
   
2. Ejecutar el servidor en una terminal:

python server.py


3. Ejecutar el cliente en otra terminal:

python cliente.py


4. Escribir mensajes en el cliente.

El servidor los guarda en chat.db.

Responde con: Mensaje recibido: <timestamp>

5. Para salir, escribir:

éxito
