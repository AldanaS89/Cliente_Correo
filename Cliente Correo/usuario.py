from carpeta import Carpeta
import heapq  # Se usa para la cola de prioridad

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena

        # Carpetas principales
        self._recibidos = Carpeta("Recibidos")
        self._enviados = Carpeta("Enviados")

        # Lista de filtros automáticos y cola de prioridad para urgentes
        self._filtros = []        # Guarda reglas en forma de diccionario
        self._cola_urgentes = []  # Almacena mensajes urgentes (prioridad 1)

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena

    # Agregar un filtro automático
    def agregar_filtro(self, palabra_clave, carpeta_destino):
        # Cada filtro tiene una palabra y una carpeta destino
        regla = {"palabra": palabra_clave, "destino": carpeta_destino}
        self._filtros.append(regla)

    # Aplicar filtros al recibir un mensaje
    def aplicar_filtros(self, mensaje):
        for filtro in self._filtros:
            if filtro["palabra"].lower() in mensaje.asunto.lower():
                destino = self._recibidos.obtener_subcarpeta(filtro["destino"])
                if destino is None:
                    destino = Carpeta(filtro["destino"])
                    self._recibidos.agregar_subcarpeta(destino)
                destino.agregar_mensaje(mensaje)
                return True
        return False

    def recibir(self, mensaje):
        # Si es urgente se agrega a la cola de prioridad
        if mensaje.prioridad == 1:
            heapq.heappush(self._cola_urgentes, (mensaje.prioridad, mensaje))
        # Si no es urgente, aplicamos filtros o lo guardamos normalmente
        elif not self.aplicar_filtros(mensaje):
            self._recibidos.agregar_mensaje(mensaje)

    # Procesar mensajes urgentes (sacarlos de la cola y guardarlos)
    def procesar_urgentes(self):
        while self._cola_urgentes:
            _, mensaje = heapq.heappop(self._cola_urgentes)
            self._recibidos.agregar_mensaje(mensaje)

    def recibir_enviado(self, mensaje):
        self._enviados.agregar_mensaje(mensaje)

    def listar_inbox(self):
        return self._recibidos.listar_mensajes()

    def listar_enviados(self):
        return self._enviados.listar_mensajes()

    def buscar_mensajes(self, asunto=None, remitente=None):
        resultados = []
        resultados.extend(self._recibidos.buscar_mensajes(asunto, remitente))
        resultados.extend(self._enviados.buscar_mensajes(asunto, remitente))
        return resultados

    def mover_mensaje(self, mensaje, carpeta_origen, carpeta_destino):
        return carpeta_origen.mover_mensaje(mensaje, carpeta_destino)