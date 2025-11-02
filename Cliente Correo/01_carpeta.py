# Clase que representa una carpeta (por ejemplo: Recibidos, Enviados)

from mensaje import Mensaje

class Carpeta:
    def __init__(self, nombre):
        # Cada carpeta tiene un nombre, una lista de mensajes y subcarpetas
        self._nombre = nombre
        self._mensajes = []
        self._subcarpetas = []

    @property
    def nombre(self):
        return self._nombre

    # Agrega un mensaje a la carpeta
    def agregar_mensaje(self, mensaje):
        self._mensajes.append(mensaje)

    # Crea y agrega una subcarpeta dentro de esta carpeta
    def agregar_subcarpeta(self, subcarpeta):
        self._subcarpetas.append(subcarpeta)

    # Busca una subcarpeta por nombre (nivel directo)
    def obtener_subcarpeta(self, nombre):
        for sub in self._subcarpetas:
            if sub.nombre == nombre:
                return sub
        return None

    # Lista los mensajes de la carpeta actual
    def listar_mensajes(self):
        return [m.resumen() for m in self._mensajes]

    # Busca mensajes de forma recursiva por asunto o remitente
    def buscar_mensajes(self, asunto=None, remitente=None):
        resultados = []

        # Busca coincidencias en los mensajes de la carpeta actual
        for mensaje in self._mensajes:
            if (asunto is None or asunto.lower() in mensaje.asunto.lower()) and \
               (remitente is None or remitente.lower() in mensaje.remitente.lower()):
                resultados.append(mensaje)

        # Llama recursivamente a las subcarpetas
        for subcarpeta in self._subcarpetas:
            resultados.extend(subcarpeta.buscar_mensajes(asunto, remitente))

        return resultados

    # Mueve un mensaje a otra carpeta (buscando recursivamente si es necesario)
    def mover_mensaje(self, mensaje, carpeta_destino):
        # Si el mensaje está en esta carpeta, lo movemos directamente
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            return True

        # Si no está, lo buscamos en las subcarpetas (recursividad)
        for subcarpeta in self._subcarpetas:
            if subcarpeta.mover_mensaje(mensaje, carpeta_destino):
                return True

        # Si no se encontró el mensaje en esta rama del árbol
        return False
