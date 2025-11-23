from carpeta import Carpeta
from mensaje import Mensaje
from datetime import datetime, timedelta

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena

        # Carpetas principales
        self._recibidos = Carpeta("Recibidos")
        self._enviados = Carpeta("Enviados")
        self._papelera = Carpeta("Papelera")

        # Carpetas personalizadas
        self._carpetas_personalizadas = {}

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def recibidos(self):
        return self._recibidos

    @property
    def enviados(self):
        return self._enviados

    @property
    def papelera(self):
        self._eliminar_viejos_papelera()
        return self._papelera

    @property
    def carpetas_personalizadas(self):
        return self._carpetas_personalizadas

    def enviar_mensaje(self, destinatario, asunto, contenido, prioridad=2):
        mensaje = Mensaje(self._correo, destinatario, asunto, contenido, prioridad)
        self._enviados.agregar_mensaje(mensaje)
        return mensaje

    def recibir_mensaje(self, mensaje):
        self._recibidos.agregar_mensaje(mensaje)

    def crear_carpeta(self, nombre):
        if nombre in self._carpetas_personalizadas:
            return False
        self._carpetas_personalizadas[nombre] = Carpeta(nombre)
        return True

    def borrar_carpeta(self, nombre):
        if nombre not in self._carpetas_personalizadas:
            return False
        carpeta = self._carpetas_personalizadas[nombre]
        if not carpeta.esta_vacia():
            return False
        del self._carpetas_personalizadas[nombre]
        return True

    def mover_mensaje(self, carpeta_origen, carpeta_destino, mensaje):
        if mensaje in carpeta_origen.mensajes:
            carpeta_origen.eliminar_mensaje(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            return True
        return False

    def _eliminar_viejos_papelera(self):
        ahora = datetime.now()
        nuevos = []
        for msg in self._papelera.mensajes:
            if ahora - msg.fecha < timedelta(days=30):
                nuevos.append(msg)
        self._papelera._mensajes = nuevos
