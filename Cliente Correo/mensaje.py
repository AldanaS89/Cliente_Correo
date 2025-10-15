# Clase que representa un mensaje de correo electrónico

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido):
        # Se guardan los datos del mensaje
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido

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

    # Devuelve un resumen corto del mensaje
    def resumen(self):
        return f"Asunto: {self._asunto} (de {self._remitente})"