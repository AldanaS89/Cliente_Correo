# Clase que representa a un usuario

from carpeta import Carpeta

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena

        # Carpetas principales
        self._recibidos = Carpeta("Recibidos")
        self._enviados = Carpeta("Enviados")

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena

    def enviar(self, correo_destinatario, asunto, contenido, servidor):
        return servidor.enviar_mensaje(self, correo_destinatario, asunto, contenido)

    def recibir(self, mensaje):
        self._recibidos.agregar_mensaje(mensaje)

    def recibir_enviado(self, mensaje):
        self._enviados.agregar_mensaje(mensaje)

    def listar_inbox(self):
        return self._recibidos.listar_mensajes()

    def listar_enviados(self):
        return self._enviados.listar_mensajes()

    # Permite buscar mensajes en todas las carpetas (recursivamente)
    def buscar_mensajes(self, asunto=None, remitente=None):
        resultados = []
        resultados.extend(self._recibidos.buscar_mensajes(asunto, remitente))
        resultados.extend(self._enviados.buscar_mensajes(asunto, remitente))
        return resultados

    # Permite mover un mensaje entre carpetas (por ejemplo de Recibidos a Enviados)
    def mover_mensaje(self, mensaje, carpeta_origen, carpeta_destino):
        return carpeta_origen.mover_mensaje(mensaje, carpeta_destino)