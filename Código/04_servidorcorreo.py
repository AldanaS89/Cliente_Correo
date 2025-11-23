from mensaje import Mensaje
from usuario import Usuario
from collections import deque   # Para BFS (cola FIFO)

class ServidorCorreo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._usuarios = {}      # correo -> Usuario
        self._red = {}           # grafo: servidor -> lista de servidores vecinos
        self._red[self._nombre] = []  # nodo propio

    @property
    def nombre(self):
        return self._nombre

    # CONEXIÓN DE SERVIDORES
    def agregar_conexion(self, otro_servidor): #Conecta este servidor con otro (grafo no dirigido).
        if otro_servidor.nombre not in self._red:
            self._red[otro_servidor.nombre] = []
        if self._nombre not in otro_servidor._red:
            otro_servidor._red[self._nombre] = []

        if otro_servidor.nombre not in self._red[self._nombre]:
            self._red[self._nombre].append(otro_servidor.nombre)
        if self._nombre not in otro_servidor._red[otro_servidor.nombre]:
            otro_servidor._red[otro_servidor.nombre].append(self._nombre)

    def mostrar_red(self):
        return self._red

    # RUTA ENTRE SERVIDORES (BFS)
    def ruta_BFS(self, inicio, destino):
        visitados = set()
        cola = deque([[inicio]])

        while cola:
            camino = cola.popleft()
            nodo_actual = camino[-1]

            if nodo_actual == destino:
                return camino

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for vecino in self._red.get(nodo_actual, []):
                    nuevo = list(camino)
                    nuevo.append(vecino)
                    cola.append(nuevo)

        return None  # Sin ruta disponible

    # GESTIÓN DE USUARIOS
    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            return False, "El usuario ya existe."
        self._usuarios[correo] = Usuario(nombre, correo, contrasena)
        return True, "Usuario registrado exitosamente."

    def iniciar_sesion(self, correo, contrasena):
        if correo not in self._usuarios:
            return None, "Correo no registrado."
        usuario = self._usuarios[correo]
        if not usuario.verificar_contrasena(contrasena):
            return None, "Contraseña incorrecta."
        return usuario, "Inicio de sesión exitoso."

    def listar_usuarios(self):
        return list(self._usuarios.keys())

    def usuario_existente(self, correo):
        return correo in self._usuarios

    # ENVÍO DE MENSAJES
    def enviar_mensaje(self, remitente, correo_destinatario, asunto, contenido, prioridad=2):
        # Verificar existencia del destinatario
        if correo_destinatario not in self._usuarios:
            mensaje_error = Mensaje("Sistema", remitente.correo, asunto, "El destinatario no existe.")
            remitente.recibir_mensaje(mensaje_error)
            return False, "El destinatario no existe."

        # Verificar que haya ruta en la red
        ruta = self.ruta_BFS(self._nombre, self._nombre)  # simulado: mismo servidor
        if ruta is None:
            mensaje_error = Mensaje("Sistema", remitente.correo, asunto, "No hay ruta disponible entre servidores.")
            remitente.recibir_mensaje(mensaje_error)
            return False, "No hay ruta disponible en la red."

        # Crear mensaje
        destinatario = self._usuarios[correo_destinatario]
        mensaje = Mensaje(remitente.correo, destinatario.correo, asunto, contenido, prioridad)

        # Guardar en enviados y entregarlo
        remitente.enviar_mensaje(destinatario.correo, asunto, contenido, prioridad)
        destinatario.recibir_mensaje(mensaje)

        return True, "Mensaje enviado exitosamente."
