from datetime import datetime

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido, prioridad=2):
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido

        # 1 = urgente, 2 = normal
        if prioridad not in (1, 2):
            prioridad = 2
        self._prioridad = prioridad

        # Fecha exacta de envío
        self._fecha = datetime.now()

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

    # Resumen para listas (solo asunto + remitente/destinatario)
    def resumen(self, modo="recibidos"):
        if modo == "enviados":
            return f"{self._asunto} — a {self._destinatario}"
        else:
            return f"{self._asunto} — de {self._remitente}"

    # Detalle completo del mensaje
    def mostrar_detalle(self):
        etiqueta = "URGENTE" if self._prioridad == 1 else "Normal"
        return (
            f"--- MENSAJE ---\n"
            f"Asunto: {self._asunto}\n"
            f"De: {self._remitente}\n"
            f"Para: {self._destinatario}\n"
            f"Fecha de envío: {self._fecha.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Prioridad: {etiqueta}\n\n"
            f"{self._contenido}\n"
        )
