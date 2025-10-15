# Clase que simula el servidor de correo

from usuario import Usuario
from mensaje import Mensaje

class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}

    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            return False, "El usuario ya existe, ingrese otro."
        nuevo_usuario = Usuario(nombre, correo, contrasena)
        self._usuarios[correo] = nuevo_usuario
        return True, "Usuario registrado exitosamente."

    def iniciar_sesion(self, correo, contrasena):
        if correo not in self._usuarios:
            return None, "Correo no registrado."
        usuario = self._usuarios[correo]
        if not usuario.verificar_contrasena(contrasena):
            return None, "Contraseña incorrecta."
        return usuario, "Inicio de sesión exitoso."

    def enviar_mensaje(self, remitente, correo_destinatario, asunto, contenido):
        # Si el destinatario no existe, el remitente recibe un aviso
        if correo_destinatario not in self._usuarios:
            mensaje = Mensaje(remitente.correo, "desconocido", asunto, "Destinatario inexistente.")
            remitente.recibir(mensaje)
            return False, "El destinatario no existe."

        destinatario = self._usuarios[correo_destinatario]
        mensaje = Mensaje(remitente.correo, destinatario.correo, asunto, contenido)
        remitente.recibir_enviado(mensaje)
        destinatario.recibir(mensaje)
        return True, "Mensaje enviado exitosamente."
