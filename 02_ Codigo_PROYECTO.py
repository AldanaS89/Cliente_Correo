# Clase que representa un mensaje de correo electrónico
class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido):
        # Se guardan los datos del mensaje
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._contenido = contenido

    # Propiedades para acceder a los atributos de forma controlada
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


# Clase que representa una carpeta (Por ejemplo: Recibidos, Enviados)
class Carpeta:
    def __init__(self, nombre):
        # Cada carpeta tiene un nombre y una lista de mensajes
        self._nombre = nombre
        self._mensajes = []

    @property
    def nombre(self):
        return self._nombre

    # Agrega un mensaje a la carpeta
    def agregar_mensaje(self, mensaje):
        self._mensajes.append(mensaje)

    # Lista los mensajes en forma de resumen
    def listar_mensajes(self):
        return [m.resumen() for m in self._mensajes]


# Clase que representa a un usuario
class Usuario:
    def __init__(self, nombre, correo, contrasena):
        # Datos del usuario
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena
        # Cada usuario tiene dos carpetas 
        self._recibidos = Carpeta("Recibidos")
        self._enviados = Carpeta("Enviados")

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    # Verifica que la contraseña ingresada sea correcta
    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena

    # Envía un mensaje usando el servidor
    def enviar(self, correo_destinatario, asunto, contenido, servidor):
        return servidor.enviar_mensaje(self, correo_destinatario, asunto, contenido)

    # Recibe un mensaje en la carpeta "Recibidos"
    def recibir(self, mensaje):
        self._recibidos.agregar_mensaje(mensaje)

    # Guarda un mensaje en la carpeta "Enviados"
    def recibir_enviado(self, mensaje):
        self._enviados.agregar_mensaje(mensaje)

    # Lista los mensajes de la bandeja de entrada
    def listar_inbox(self):
        return self._recibidos.listar_mensajes()

    # Lista los mensajes enviados
    def listar_enviados(self):
        return self._enviados.listar_mensajes()


# Clase que simula el servidor de correo
class ServidorCorreo:
    def __init__(self):
        # Diccionario que guarda los usuarios registrados (correo: usuario)
        self._usuarios = {}

    # Registrar un nuevo usuario en el servidor
    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            return False, "El usuario ya existe, ingrese otro."
        nuevo_usuario = Usuario(nombre, correo, contrasena)
        self._usuarios[correo] = nuevo_usuario
        return True, "Usuario registrado exitosamente."

    # Iniciar sesión con correo y contraseña
    def iniciar_sesion(self, correo, contrasena):
        if correo not in self._usuarios:
            return None, "Correo no registrado."
        usuario = self._usuarios[correo]
        if not usuario.verificar_contrasena(contrasena):
            return None, "Contraseña incorrecta."
        return usuario, "Inicio de sesión exitoso."

    # Enviar un mensaje de un usuario a otro
    def enviar_mensaje(self, remitente, correo_destinatario, asunto, contenido):
        # Si el destinatario no existe, el remitente recibe un aviso
        if correo_destinatario not in self._usuarios:
            mensaje = Mensaje(remitente.correo, "desconocido", asunto, "Destinatario inexistente.")
            remitente.recibir(mensaje)
            return False, "El destinatario no existe."
        # Si existe, se crea el mensaje y se guarda en ambas carpetas
        destinatario = self._usuarios[correo_destinatario]
        mensaje = Mensaje(remitente.correo, destinatario.correo, asunto, contenido)
        remitente.recibir_enviado(mensaje)
        destinatario.recibir(mensaje)
        return True, "Mensaje enviado exitosamente."

