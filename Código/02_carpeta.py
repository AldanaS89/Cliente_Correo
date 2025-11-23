# Clase que representa una carpeta (por ejemplo: Recibidos, Enviados)
from datetime import datetime, timedelta
from mensaje import Mensaje

class Carpeta:
    def __init__(self, nombre):
        self._nombre = nombre
        self._mensajes = []          # Lista de objetos Mensaje
        self._fecha_borrado = {}     # Solo para la papelera: mensaje -> fecha en que fue movido

    @property
    def nombre(self):
        return self._nombre

    @property
    def mensajes(self):
        return self._mensajes

    def esta_vacia(self):
        return len(self._mensajes) == 0

    def agregar_mensaje(self, mensaje):
        self._mensajes.append(mensaje)
        # Registrar fecha si es papelera
        if self._nombre.lower() == "papelera":
            self._fecha_borrado[mensaje] = datetime.now()

    def eliminar_mensaje(self, mensaje):
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            if mensaje in self._fecha_borrado:
                del self._fecha_borrado[mensaje]

    def mostrar_lista(self, carpeta_padre="recibidos"):
        if self.esta_vacia():
            print(f"\nLa carpeta '{self._nombre}' está vacía.")
            return

        print(f"\n--- Mensajes en {self._nombre} ---")
        for i, m in enumerate(self._mensajes, start=1):
            extra = f"→ {m.destinatario}" if carpeta_padre.lower() == "enviados" else f"← {m.remitente}"
            print(f"{i}. {m.asunto} {extra}")

    def obtener_mensaje(self, indice):
        if 0 <= indice < len(self._mensajes):
            return self._mensajes[indice]
        return None

    def limpiar_papelera(self):
        if self._nombre.lower() != "papelera":
            return
        ahora = datetime.now()
        limite = timedelta(days=30)
        mensajes_a_borrar = [msg for msg, fecha in self._fecha_borrado.items() if ahora - fecha > limite]
        for msg in mensajes_a_borrar:
            self.eliminar_mensaje(msg)
