from mensaje import Mensaje
from usuario import Usuario
from collections import deque  # Para implementar BFS (cola)

class ServidorCorreo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._usuarios = {}
        self._red = {}  # Representa la red de servidores como grafo

    # Conectar este servidor con otros (grafo no dirigido)
    def agregar_conexion(self, otro_servidor):
        if otro_servidor not in self._red:
            self._red[otro_servidor] = []
        if self._nombre not in self._red:
            self._red[self._nombre] = []
        self._red[self._nombre].append(otro_servidor)
        self._red[otro_servidor].append(self._nombre)

    # Mostrar todas las conexiones existentes
    def mostrar_red(self):
        return self._red

    # Búsqueda en amplitud (BFS) para simular envío entre servidores
    def ruta_BFS(self, inicio, destino):
        visitados = set()
        cola = deque([[inicio]])  # Comienza desde el nodo de inicio

        while cola:
            camino = cola.popleft()
            nodo = camino[-1]
            if nodo == destino:
                return camino
            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in self._red.get(nodo, []):
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    cola.append(nuevo_camino)
        return None  # Si no hay camino

    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            return False, "El usuario ya existe."
        nuevo_usuario = Usuario(nombre, correo, contrasena)
        self._usuarios[correo] = nuevo_usuario
        return True, "Usuario registrado exitosamente."

    def iniciar_sesion(self, correo, contrasena):
        if correo not in self._usuarios:
            return None, "Correo no registrado."
        usuario = self._usuarios[correo]
        if not usuario.verificar_contrasena(contrasena):
            return None, "Contraseña incorrecta."
        return usuario, "Inicio de sesión exitoso."

    def enviar_mensaje(self, remitente, correo_destinatario, asunto, contenido, prioridad=2):
        if correo_destinatario not in self._usuarios:
            mensaje_error = Mensaje("Sistema", remitente.correo, asunto, "Destinatario inexistente.")
            remitente.recibir(mensaje_error)
            return False, "El destinatario no existe."

        destinatario = self._usuarios[correo_destinatario]
        mensaje = Mensaje(remitente.correo, destinatario.correo, asunto, contenido, prioridad)
        remitente.recibir_enviado(mensaje)
        destinatario.recibir(mensaje)
        return True, "Mensaje enviado exitosamente."