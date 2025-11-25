from mensaje import Mensaje
from usuario import Usuario
from collections import deque   # para BFS

class ServidorCorreo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._usuarios = {}        # correo -> Usuario
        self._red = {nombre: []}   # grafo (servidor -> vecinos)

    @property
    def nombre(self):
        return self._nombre

    #   GRAFO DE SERVIDORES

    def agregar_conexion(self, otro_servidor):
        # Conecta este servidor con otro en ambas direcciones (no dirigido).

        if otro_servidor.nombre not in self._red:
            self._red[otro_servidor.nombre] = []

        if self._nombre not in otro_servidor._red:
            otro_servidor._red[self._nombre] = []

        if otro_servidor.nombre not in self._red[self._nombre]:
            self._red[self._nombre].append(otro_servidor.nombre)

        if self._nombre not in otro_servidor._red.get(otro_servidor.nombre, []):
            otro_servidor._red[otro_servidor.nombre].append(self._nombre)

    def mostrar_red(self):
        return self._red

    def ruta_BFS(self, inicio, destino):
        """Devuelve la ruta más corta entre dos servidores."""
        visitados = set()
        cola = deque([[inicio]])

        while cola:
            camino = cola.popleft()
            nodo = camino[-1]

            if nodo == destino:
                return camino

            if nodo not in visitados:
                visitados.add(nodo)

                for vecino in self._red.get(nodo, []):
                    nuevo = list(camino)
                    nuevo.append(vecino)
                    cola.append(nuevo)

        return None   # no hay ruta

    #   USUARIOS

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

    def usuario_existente(self, correo):
        return correo in self._usuarios

    def listar_usuarios(self):
        return list(self._usuarios.keys())

    #   ENVÍO DE MENSAJES ENTRE USUARIOS

    def enviar_mensaje(self, remitente_usuario, correo_destinatario, asunto, contenido, prioridad=2):

        # 1) Verificar si existe el destinatario
        if correo_destinatario not in self._usuarios:
            # Enviar mensaje de error al remitente
            error = Mensaje(
                "Sistema",
                remitente_usuario.correo,
                f"Error envío: {asunto}",
                f"El destinatario {correo_destinatario} no existe."
            )
            remitente_usuario.recibir_mensaje(error)
            return False, "El destinatario no existe."

        # 2) Verificar ruta (aunque estés usando 1 servidor)
        ruta = self.ruta_BFS(self._nombre, self._nombre)
        if ruta is None:
            error = Mensaje(
                "Sistema",
                remitente_usuario.correo,
                f"Error envío: {asunto}",
                "No hay ruta disponible en la red."
            )
            remitente_usuario.recibir_mensaje(error)
            return False, "No hay ruta disponible."

        # 3) Crear mensaje y guardarlo en ENVIADOS del remitente
        msg = remitente_usuario.enviar_mensaje(
            correo_destinatario,
            asunto,
            contenido,
            prioridad
        )

        # 4) Entregar mensaje al destinatario
        destinatario_usuario = self._usuarios[correo_destinatario]
        destinatario_usuario.recibir_mensaje(msg)

        return True, "Mensaje enviado exitosamente."
