# Archivo principal del proyecto: Cliente de correo electrónico
# Autora: Aldana Benavent - Grupo 38
# Este archivo muestra cómo se integran los módulos del proyecto y permite realizar pruebas simples del sistema.

from mensaje import Mensaje
from carpeta import Carpeta
from usuario import Usuario
from servidorcorreo import ServidorCorreo
from datetime import datetime, timedelta

def menu_principal(usuario, servidor):
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ver carpetas")
        print("2. Crear carpeta personalizada")
        print("3. Borrar carpeta vacía")
        print("4. Revisar papelera (borrar mensajes > 30 días)")
        print("5. Enviar mensaje")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_carpetas(usuario)
        elif opcion == "2":
            crear_carpeta(usuario)
        elif opcion == "3":
            borrar_carpeta(usuario)
        elif opcion == "4":
            limpieza_papelera(usuario)
        elif opcion == "5":
            enviar_mensaje(usuario, servidor)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

# ---------------- MENÚ CARPETAS ----------------
def menu_carpetas(usuario):
    while True:
        print("\n=== CARPETAS ===")
        carpetas = [usuario.recibidos, usuario.enviados, usuario.papelera] + list(usuario.carpetas_personalizadas.values())
        for i, carpeta in enumerate(carpetas, start=1):
            print(f"{i}. {carpeta.nombre}")
        print("0. Volver")
        opcion = input("Seleccione carpeta: ")

        if opcion == "0":
            break
        if not opcion.isdigit() or int(opcion) -1 >= len(carpetas):
            print("Opción inválida.")
            continue

        carpeta = carpetas[int(opcion)-1]
        menu_carpeta_individual(carpeta, usuario)

def menu_carpeta_individual(carpeta, usuario):
    while True:
        print(f"\n=== Carpeta: {carpeta.nombre} ===")
        if carpeta.esta_vacia():
            print("La carpeta está vacía.")
            print("0. Volver")
            if input("> ") == "0":
                break
            else:
                continue
        for i, msg in enumerate(carpeta.mensajes, start=1):
            if carpeta.nombre.lower() == "enviados":
                extra = f"Para: {msg.destinatario}"
            else:
                extra = f"De: {msg.remitente}"
            print(f"{i}. {msg.asunto} | {extra} | Fecha: {msg.fecha}")
        print("L. Leer mensaje")
        print("M. Mover mensaje")
        print("0. Volver")
        opcion = input("Seleccione: ").lower()
        if opcion == "0":
            break
        elif opcion == "l":
            leer_mensaje(carpeta)
        elif opcion == "m":
            mover_mensaje(carpeta, usuario)
        else:
            print("Opción inválida.")

def leer_mensaje(carpeta):
    indice = input("Número del mensaje a leer: ")
    if not indice.isdigit():
        print("Entrada inválida.")
        return
    indice = int(indice)-1
    if indice <0 or indice >= len(carpeta.mensajes):
        print("Mensaje inexistente.")
        return
    msg = carpeta.mensajes[indice]
    print("\n--- MENSAJE ---")
    print(f"Asunto: {msg.asunto}")
    print(f"De: {msg.remitente}" if carpeta.nombre.lower()!="enviados" else f"Para: {msg.destinatario}")
    print(f"Fecha: {msg.fecha}")
    print(f"Cuerpo:\n{msg.cuerpo}")
    print("--------------")

def mover_mensaje(carpeta_origen, usuario):
    indice = input("Número del mensaje a mover: ")
    if not indice.isdigit():
        print("Entrada inválida.")
        return
    indice = int(indice)-1
    if indice <0 or indice>=len(carpeta_origen.mensajes):
        print("Mensaje inexistente.")
        return
    msg = carpeta_origen.mensajes[indice]
    print("\nMover a qué carpeta?")
    carpetas = [usuario.recibidos, usuario.enviados, usuario.papelera] + list(usuario.carpetas_personalizadas.values())
    for i, c in enumerate(carpetas, start=1):
        print(f"{i}. {c.nombre}")
    opcion = input("> ")
    if not opcion.isdigit() or int(opcion)-1 >= len(carpetas):
        print("Opción inválida.")
        return
    carpeta_destino = carpetas[int(opcion)-1]
    carpeta_origen.eliminar_mensaje(msg)
    carpeta_destino.agregar_mensaje(msg)
    print("Mensaje movido.")

# ----------------- CREAR/BORRAR CARPETAS -----------------
def crear_carpeta(usuario):
    nombre = input("Nombre nueva carpeta: ").strip()
    if usuario.crear_carpeta(nombre):
        print("Carpeta creada.")
    else:
        print("Ya existe carpeta con ese nombre.")

def borrar_carpeta(usuario):
    personal = [c for c in usuario.carpetas_personalizadas.values() if c.esta_vacia()]
    if not personal:
        print("No hay carpetas vacías para borrar.")
        return
    for i,c in enumerate(personal, start=1):
        print(f"{i}. {c.nombre}")
    opcion = input("Seleccione: ")
    if not opcion.isdigit() or int(opcion)-1 >= len(personal):
        print("Opción inválida.")
        return
    usuario.borrar_carpeta(personal[int(opcion)-1].nombre)
    print("Carpeta eliminada.")

# ----------------- LIMPIEZA PAPELERA -----------------
def limpieza_papelera(usuario):
    papelera = usuario.papelera
    papelera.limpiar_papelera()
    print("Limpieza realizada.")

# ----------------- ENVÍO DE MENSAJE -----------------
def enviar_mensaje(usuario, servidor):
    destinatario = input("Correo destinatario: ").strip()
    asunto = input("Asunto: ").strip()
    cuerpo = input("Cuerpo del mensaje: ").strip()
    exito, msg = servidor.enviar_mensaje(usuario, destinatario, asunto, cuerpo)
    print(msg)

# ----------------- PROGRAMA PRINCIPAL -----------------
if __name__ == "__main__":
    # Crear servidor
    servidor = ServidorCorreo("Servidor1")

    # Crear usuario demo
    exito, msg = servidor.registrar_usuario("Aldana", "aldana@mail.com", "123")
    usuario, msg_login = servidor.iniciar_sesion("aldana@mail.com", "123")

    # Lanzar menú
    menu_principal(usuario, servidor)
