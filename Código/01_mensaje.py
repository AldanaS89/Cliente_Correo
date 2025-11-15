from datetime import datetime

# Clase que representa un mensaje de correo electrónico
class Mensaje:
    
    def __init__(self, remitente, destinatario, asunto, contenido, prioridad=2):
        # Atributos principales del mensaje
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido

        # Prioridad (1 = urgente, 2 = normal). Validamos valores incorrectos.
        if prioridad not in (1, 2):
            prioridad = 2
        self._prioridad = prioridad

        # Fecha y hora exacta en que el mensaje fue enviado
        self._fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    # Propiedades para acceder a los atributos(encapsulamiento)
    @property
    def remitente(self):
        return self._remitente

    @property
    def destinatario(self):
        return self._destinatario

    @property
    def asunto(self):
        return self._asunto

    @property
    def contenido(self):
        return self._contenido

    @property
    def prioridad(self):
        return self._prioridad

    @property
    def fecha(self):
        return self._fecha

    # Devuelve un resumen corto del mensaje
    def resumen(self):
        # Muestra si el mensaje es urgente
        etiqueta = " (URGENTE)" if self._prioridad == 1 else ""
        return f"[{self._fecha}] {self._asunto}{etiqueta} — de {self._remitente}"    
        
# Muestra detalle completo del mensaje
    def mostrar_detalle(self):
        etiqueta = "URGENTE" if self._prioridad == 1 else "Normal"
        return (
            f"--- MENSAJE ---\n"
            f"De: {self._remitente}\n"
            f"Para: {self._destinatario}\n"
            f"Asunto: {self._asunto}\n"
            f"Prioridad: {etiqueta}\n"
            f"Fecha de envío: {self._fecha}\n"
            f"Contenido:\n{self._contenido}\n"
        )
