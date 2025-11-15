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
        self._papelera = Carpeta("Papelera")

        # Lista de filtros automáticos y cola de prioridad para urgentes
        self._filtros = []        # Guarda reglas en forma de diccionario
        self._cola_urgentes = []  # Almacena mensajes urgentes (prioridad 1)

    # Encapsulamiento de atributos
    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena
    
    # Manejo de carpetas
    def crear_carpeta(self, nombre):
        nueva = Carpeta(nombre)
        self._recibidos.agregar_subcarpeta(nueva)
        return nueva
    
    def obtener_carpeta(self, nombre):
        if nombre == "Recibidos":
            return self._recibidos
        elif nombre == "Enviados":
            return self._enviados
        elif nombre == "Papelera":
            return self._papelera

        # Buscar recursivamente en subcarpetas
        return self._recibidos.obtener_subcarpeta(nombre)
    
    def listar_carpetas(self):
        lista = ["Recibidos", "Enviados", "Papelera"]
        lista.extend(self._recibidos.listar_subcarpetas())
        return lista

    # Agregar un filtro automático
    def agregar_filtro(self, palabra_clave, carpeta_destino):
        regla = {"palabra": palabra_clave, "destino": carpeta_destino}
        self._filtros.append(regla)

    def aplicar_filtros(self, mensaje):
        for filtro in self._filtros:
            if filtro["palabra"].lower() in mensaje.asunto.lower():
                destino = self.obtener_carpeta(filtro["destino"])
                # Si la carpeta no existe, la creamos
                if destino is None:
                    destino = self.crear_carpeta(filtro["destino"])
                destino.agregar_mensaje(mensaje)
                return True
        return False

    # Recepción de mensajes
    def recibir(self, mensaje):
        # Los urgentes van a la cola de prioridad
        if mensaje.prioridad == 1:
            heapq.heappush(self._cola_urgentes, (mensaje.prioridad, mensaje))
        # Los normales intentan pasar por filtros
        elif not self.aplicar_filtros(mensaje):
            self._recibidos.agregar_mensaje(mensaje)

    def procesar_urgentes(self):
        #Pasa los urgentes desde la cola a Recibidos.
        while self._cola_urgentes:
            _, mensaje = heapq.heappop(self._cola_urgentes)
            self._recibidos.agregar_mensaje(mensaje)

    def ver_urgentes_pendientes(self):
        return [datos[1].resumen() for datos in self._cola_urgentes]

    # Envío y consultas
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

    # Mover y borrar mensajes
    def mover_mensaje(self, mensaje, carpeta_origen, carpeta_destino):
        return carpeta_origen.mover_mensaje(mensaje, carpeta_destino)

    def borrar_mensaje(self, mensaje, carpeta_origen):
        carpeta_origen.mover_mensaje(mensaje, self._papelera)
