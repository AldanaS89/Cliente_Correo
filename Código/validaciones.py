# Validaciones al registrar e iniciar sesión

import re

def registro_valido(servidor):
    while True:
        nombre = input("Nombre completo: ").strip()
        if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+", nombre):
            print("Nombre inválido. Solo letras y espacios permitidos.")
            continue

        correo = input("Correo: ").strip()
        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@mail\.com", correo):
            print("Correo inválido. Debe terminar en @mail.com")
            continue
        if servidor.usuario_existente(correo):
            print("Correo ya registrado.")
            continue

        contrasena = input("Contraseña: ").strip()
        if not contrasena:
            print("Contraseña no puede estar vacía.")
            continue

        exito, msg = servidor.registrar_usuario(nombre, correo, contrasena)
        print(msg)
        if exito:
            break

def login(servidor):
    correo = input("Correo: ").strip()
    contrasena = input("Contraseña: ").strip()

    usuario, msg = servidor.iniciar_sesion(correo, contrasena)
    print(msg)

    if usuario:
        return usuario
    return None