from mensaje import Mensaje
from usuario import Usuario
from collections import deque
import heapq  

class ServidorCorreo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._usuarios = {}        # correo -> Usuario
        self._red = {nombre: []}   # grafo (servidor -> vecinos)
        self._cola_envios = []     

    @property
    def nombre(self):
        return self._nombre

    #   GRAFO DE SERVIDORES (Rutas y Conexiones)

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

    #   GESTIÓN DE USUARIOS

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

    #   ENVÍO Y PROCESAMIENTO DE MENSAJES

    def enviar_mensaje(self, remitente_usuario, correo_destinatario, asunto, contenido, prioridad=2):

        # 1) Verificar si existe el destinatario
        if correo_destinatario not in self._usuarios:
            error = Mensaje(
                "Sistema",
                remitente_usuario.correo,
                f"Error envío: {asunto}",
                f"El destinatario {correo_destinatario} no existe."
            )
            # Los errores de sistema se entregan inmediatamente al remitente
            remitente_usuario.recibir_mensaje(error)
            return False, "El destinatario no existe."

        # 2) Verificar ruta
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

        # 3) Crear mensaje y guardarlo en la carpeta ENVIADOS del remitente
        msg = remitente_usuario.enviar_mensaje(
            correo_destinatario,
            asunto,
            contenido,
            prioridad
        )

        # 4) ENCOLAR
        # Guardamos una tupla: (Prioridad, Fecha, Mensaje)
        # heapq ordena basándose en el primer elemento de la tupla.
        # Prioridad 1 (Urgente) saldrá antes que Prioridad 2 (Normal).
        heapq.heappush(self._cola_envios, (msg.prioridad, msg.fecha, msg))

        return True, "Mensaje puesto en cola de espera (será enviado al procesar)."

    def procesar_cola(self):
        # Procesa los mensajes pendientes en la cola de prioridad. Los mensajes urgentes saldrán primero.

        cantidad = len(self._cola_envios)
        
        if cantidad == 0:
            return # No hacer nada si está vacía
            
        print(f"\n[Servidor] Procesando {cantidad} mensajes en cola...")

        while self._cola_envios:
            # heappop extrae SIEMPRE el elemento con el número menor (Prioridad 1)
            # independientemente de cuándo entró.
            prioridad, fecha, msg = heapq.heappop(self._cola_envios)
            
            # Verificamos nuevamente que el usuario exista (seguridad extra)
            if msg.destinatario in self._usuarios:
                destinatario_usuario = self._usuarios[msg.destinatario]
                destinatario_usuario.recibir_mensaje(msg)
                print(f" -> Entregado: '{msg.asunto}' a {msg.destinatario} (Prio: {prioridad})")
            else:
                print(f" -> Error: El usuario {msg.destinatario} ya no existe. Mensaje descartado.")

        print("[Servidor] Cola de envíos vacía.")
