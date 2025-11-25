from mensaje import Mensaje
from datetime import datetime, timedelta

class Carpeta:
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self._mensajes = []           
        self._subcarpetas = {}        
        self._padre = padre            
        self._fecha_borrado = {}      

    #                   MENSAJES

    def agregar_mensaje(self, mensaje):
        self._mensajes.append(mensaje)
        self._mensajes.sort(key=lambda m: m.fecha, reverse=True)

        if self.nombre.lower() == "papelera":
            self._fecha_borrado[mensaje] = datetime.now()

    def eliminar_mensaje(self, indice_or_msg):
        if isinstance(indice_or_msg, int):
            if 0 <= indice_or_msg < len(self._mensajes):
                return self._mensajes.pop(indice_or_msg)
            return None
        else:
            msg = indice_or_msg
            if msg in self._mensajes:
                self._mensajes.remove(msg)
                if msg in self._fecha_borrado:
                    del self._fecha_borrado[msg]
                return True
            return False

    def obtener_mensajes(self):
        return list(self._mensajes)

    def esta_vacia(self):
        return len(self._mensajes) == 0 and len(self._subcarpetas) == 0

    #                 SUBCARPETAS

    def crear_subcarpeta(self, nombre):
        if nombre in self._subcarpetas:
            return False, "Ya existe una carpeta con ese nombre."
        nueva = Carpeta(nombre, padre=self)
        self._subcarpetas[nombre] = nueva
        return True, "Carpeta creada."

    def agregar_subcarpeta(self, carpeta_obj):
        if carpeta_obj.nombre in self._subcarpetas:
            return False, "Ya existe una Carpeta con ese nombre."
        carpeta_obj._padre = self
        self._subcarpetas[carpeta_obj.nombre] = carpeta_obj
        return True, "Carpeta agregada."

    def borrar_subcarpeta(self, nombre):
        if nombre not in self._subcarpetas:
            return False, "No existe esa subcarpeta."

        sub = self._subcarpetas[nombre]

        if not sub.esta_vacia():
            print(f"\nLa carpeta '{nombre}' contiene subcarpetas o mensajes.")
            print("¿Desea eliminarla COMPLETAMENTE junto a todo su contenido?")
            opcion = input("Confirmar eliminación (S/N): ").strip().lower()

            if opcion != "s":
                return False, "Cancelado por el usuario."

        del self._subcarpetas[nombre]
        return True, f"Carpeta '{nombre}' eliminada correctamente."

    def listar_subcarpetas(self):
        return list(self._subcarpetas.keys())

    def obtener_subcarpeta(self, nombre):
        return self._subcarpetas.get(nombre)

    def obtener_subcarpetas(self):
        return self._subcarpetas

    def mover_subcarpeta(self, nombre, carpeta_destino):
        if nombre not in self._subcarpetas:
            return False, "No existe esa subcarpeta aquí."

        sub = self._subcarpetas[nombre]

        # Evitar mover dentro de sí misma o hijas
        destino = carpeta_destino
        while destino is not None:
            if destino is sub:
                return False, "No puedes mover una carpeta dentro de sí misma o de sus hijas."
            destino = destino._padre

        if sub.nombre in carpeta_destino._subcarpetas:
            return False, "El destino ya contiene una carpeta con ese nombre."

        del self._subcarpetas[nombre]
        carpeta_destino._subcarpetas[nombre] = sub
        sub._padre = carpeta_destino

        return True, "Carpeta movida."

    #           BUSCAR / MOVER MENSAJES

    def buscar_mensajes(self, texto):
    
        # Busca el 'texto' dentro del asunto o del remitente. (Búsqueda recursiva en subcarpetas)
        texto = texto.lower()
        resultados = []

        # 1. Buscar en los mensajes de ESTA carpeta
        for m in self._mensajes:
            en_asunto = texto in m.asunto.lower()
            en_remitente = texto in m.remitente.lower()
            
            # Usamos OR: si aparece en uno u otro, sirve.
            if en_asunto or en_remitente:
                resultados.append(m)

        # 2. Buscar recursivamente en las subcarpetas
        for sub in self._subcarpetas.values():
            resultados.extend(sub.buscar_mensajes(texto))

        return resultados

    def mover_mensaje(self, mensaje, carpeta_destino):
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            if mensaje in self._fecha_borrado:
                del self._fecha_borrado[mensaje]
            return True

        for sub in self._subcarpetas.values():
            if sub.mover_mensaje(mensaje, carpeta_destino):
                return True

        return False

    #                  PAPELERA

    def limpiar_papelera(self):
        if self.nombre.lower() != "papelera":
            return
        
        ahora = datetime.now()
        umbral = timedelta(days=30)

        para_borrar = [
            m for m, f in list(self._fecha_borrado.items())
            if ahora - f > umbral
        ]

        for m in para_borrar:
            if m in self._mensajes:
                self._mensajes.remove(m)
            if m in self._fecha_borrado:
                del self._fecha_borrado[m]

    def __repr__(self):
        return f"Carpeta('{self.nombre}')"
