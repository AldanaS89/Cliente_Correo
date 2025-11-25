from datetime import datetime

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido, prioridad=2):
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido
        self._prioridad = prioridad if prioridad in (1, 2) else 2
        self._fecha = datetime.now()  # datetime para comparaciones y formateo al mostrar

    # Propiedades (encapsulamiento)
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

    # Resumen breve para listados 
    def resumen(self, modo="recibidos"):
        if modo == "enviados":
            return f"{self._asunto} — a {self._destinatario}"
        return f"{self._asunto} — de {self._remitente}"

    # Detalle completo mostrado al abrir el mensaje 
    def mostrar_detalle(self):
        etiqueta = "URGENTE" if self._prioridad == 1 else "Normal"
        fecha_str = self._fecha.strftime("%d/%m/%Y %H:%M:%S")
        return (
            f"--- MENSAJE ---\n"
            f"Asunto: {self._asunto}\n"
            f"De: {self._remitente}\n"
            f"Para: {self._destinatario}\n"
            f"Fecha de envío: {fecha_str}\n"
            f"Prioridad: {etiqueta}\n\n"
            f"{self._contenido}\n"
        )

    def __repr__(self):
        return f"<Mensaje '{self._asunto}' de {self._remitente} @ {self._fecha.strftime('%Y-%m-%d %H:%M:%S')}>"
