from mensaje import Mensaje
from usuario import Usuario
from collections import deque   # Para BFS (cola FIFO)

class ServidorCorreo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._usuarios = {}      # Guarda usuarios por correo
        self._red = {}           # Grafo: servidor → lista de servidores vecinos

        # Agregar el propio servidor como nodo en el grafo
        self._red[self._nombre] = []

    @property
    def nombre(self):
        return self._nombre

    # Conexión de Servidores (Grafo)
    def agregar_conexion(self, otro_servidor):
        """Conecta este servidor con otro (grafo no dirigido)."""
        
        # Crear nodos si no existen
        if otro_servidor.nombre not in self._red:
            self._red[otro_servidor.nombre] = []
        if self._nombre not in otro_servidor._red:
            otro_servidor._red[self._nombre] = []

        # Conexión bidireccional
        self._red[self._nombre].append(otro_servidor.nombre)
        otro_servidor._red[otro_servidor.nombre].append(self._nombre)

    def mostrar_red(self):
        """Devuelve el grafo completo."""
        return self._red

    # BFS para encontrar ruta entre servidores
    def ruta_BFS(self, inicio, destino):
        """Devuelve el camino entre servidores usando BFS."""
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

    # Gestión de usuarios
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

    def listar_usuarios(self):
        """Devuelve los correos de los usuarios registrados."""
        return list(self._usuarios.keys())

    # Envío de Mensajes
    def enviar_mensaje(self, remitente, correo_destinatario, asunto, contenido, prioridad=2):
        """
        Simula el envío verificando la ruta en la red de servidores.
        Para este proyecto, trabajamos con un único servidor,
        pero mantenemos BFS para demostrar estructura de datos.
        """

        # Confirmar existencia del destinatario
        if correo_destinatario not in self._usuarios:
            mensaje_error = Mensaje("Sistema", remitente.correo, asunto, "El destinatario no existe.")
            remitente.recibir(mensaje_error)
            return False, "El destinatario no existe."

        # Verificar ruta disponible en la red (a sí mismo en este proyecto)
        ruta = self.ruta_BFS(self._nombre, self._nombre)
        if ruta is None:
            mensaje_error = Mensaje("Sistema", remitente.correo, asunto, "No hay ruta disponible entre servidores.")
            remitente.recibir(mensaje_error)
            return False, "No hay ruta disponible en la red."

        # Realizar el envío
        destinatario = self._usuarios[correo_destinatario]
        mensaje = Mensaje(remitente.correo, destinatario.correo, asunto, contenido, prioridad)

        # Guardar en enviados
        remitente.recibir_enviado(mensaje)

        # Entregar al destinatario
        destinatario.recibir(mensaje)

        return True, "Mensaje enviado exitosamente."