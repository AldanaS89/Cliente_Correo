# Clase que representa un mensaje de correo electrónico

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido, prioridad=2):
        # Se guardan los datos del mensaje
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido
        self._prioridad = prioridad  # Prioridad (1 = urgente, 2 = normal)

    # Propiedades para acceder a los atributos
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

    # Devuelve un resumen corto del mensaje
    def resumen(self):
        # Muestra si el mensaje es urgente
        etiqueta = " (URGENTE)" if self._prioridad == 1 else ""
        return f"Asunto: {self._asunto}{etiqueta} (de {self._remitente})"
