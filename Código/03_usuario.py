from carpeta import Carpeta
from mensaje import Mensaje

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena

        # Carpetas base principales
        self.recibidos = Carpeta("Recibidos")
        self.enviados = Carpeta("Enviados")
        self.papelera = Carpeta("Papelera")
        
        # Filtros automáticos (remitente -> carpeta destino)
        self.filtros_remitente = {}

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena

    #  --- GESTIÓN DE FILTROS  ---

    def agregar_filtro(self, email_remitente, carpeta_destino):
        # Asocia un email a una carpeta para filtrado automático.
        if carpeta_destino.nombre == "Enviados":
            return False, "No puedes filtrar hacia Enviados."
        
        # Guardamos la regla en el diccionario hash 
        self.filtros_remitente[email_remitente] = carpeta_destino
        return True, f"Filtro guardado: {email_remitente} -> {carpeta_destino.nombre}"

    #  --- ENVÍO Y RECEPCIÓN ---

    def enviar_mensaje(self, destinatario, asunto, contenido, prioridad=2):
        msg = Mensaje(self._correo, destinatario, asunto, contenido, prioridad)
        self.enviados.agregar_mensaje(msg)
        return msg

    def recibir_mensaje(self, mensaje: Mensaje):
        # 1. Lógica de FILTROS (Prioridad Máxima)
        remitente = mensaje.remitente
        
        if remitente in self.filtros_remitente:
            # Primero: Identificamos la carpeta principal del filtro (Ej: "Jefe")
            carpeta_destino = self.filtros_remitente[remitente]

            # --- Urgentes DENTRO del Filtro ---
            if mensaje.prioridad == 1:
                # Verificamos si esa carpeta destino ya tiene una subcarpeta "Urgentes"
                if "Urgentes" not in carpeta_destino.obtener_subcarpetas():
                    carpeta_destino.crear_subcarpeta("Urgentes")
                
                # Cambiamos el destino final para que sea esa subcarpeta
                carpeta_destino = carpeta_destino.obtener_subcarpeta("Urgentes")

            # Guardamos el mensaje (ya sea en la carpeta madre o en su subcarpeta Urgentes)
            carpeta_destino.agregar_mensaje(mensaje)
            return

        # 2. Lógica de URGENTES GENÉRICOS (Solo si no tenía filtro)
        # (Esto se ejecuta si el mensaje NO es de alguien filtrado pero SÍ es urgente)
        if mensaje.prioridad == 1:
            if "Urgentes" not in self.recibidos.obtener_subcarpetas():
                self.recibidos.crear_subcarpeta("Urgentes")
            
            carpeta_urgente = self.recibidos.obtener_subcarpeta("Urgentes")
            carpeta_urgente.agregar_mensaje(mensaje)
            return

        # 3. Normal a Recibidos 
        self.recibidos.agregar_mensaje(mensaje)

    #  --- MÉTODOS AUXILIARES ---

    # Helper para obtener carpetas planas (útil para mover mensajes)
    def obtener_todas_carpetas(self):
        # Retorna un diccionario con todas las carpetas disponibles para mover mensajes
        carpetas = {
            "Recibidos": self.recibidos,
            "Enviados": self.enviados,
            "Papelera": self.papelera
        }
        # Agregamos subcarpetas de recibidos (incluyendo Urgentes si existe)
        for nombre, sub in self.recibidos.obtener_subcarpetas().items():
            carpetas[nombre] = sub
        return carpetas

    def obtener_arbol_destinos(self):
        # Genera una lista plana de todas las carpetas y subcarpetas para usarla en menús.
        # Retorna: lista de tuplas (nombre_visual, objeto_carpeta)

        lista_destinos = []

        # Función auxiliar recursiva interna
        def _recorrer(carpeta_actual, nivel):
            # Creamos un prefijo visual (ej: "Recibidos", "-- Trabajo", "---- Proyectos")
            prefijo = "-- " * nivel
            nombre_visual = f"{prefijo}{carpeta_actual.nombre}"
            
            # Guardamos la tupla (Nombre para mostrar, Objeto real)
            lista_destinos.append((nombre_visual, carpeta_actual))

            # Recorremos sus hijos
            for sub in carpeta_actual.obtener_subcarpetas().values():
                _recorrer(sub, nivel + 1)

        # Iniciamos el recorrido desde las carpetas base
        _recorrer(self.recibidos, 0)
        _recorrer(self.enviados, 0)
        # Opcional: _recorrer(self.papelera, 0) 

        return lista_destinos

    # Búsqueda global
    def buscar_mensajes(self, texto):
        resultados = []
        # Buscar en las 3 principales (la recursión de Carpeta se encarga de las subcarpetas)
        resultados.extend(self.recibidos.buscar_mensajes(texto))
        resultados.extend(self.enviados.buscar_mensajes(texto))
        resultados.extend(self.papelera.buscar_mensajes(texto))
        return resultados

    def limpiar_papelera(self):
        self.papelera.limpiar_papelera()
