# Archivo principal del proyecto: Cliente de correo electrónico
# Autora: Aldana Benavent - Grupo 38
# Este archivo muestra cómo se integran los módulos del proyecto y permite realizar pruebas simples del sistema.

from mensaje import Mensaje
from usuario import Usuario
from servidorcorreo import ServidorCorreo

def main():

    # Crear servidor y usuarios
    servidor = ServidorCorreo("ServidorCentral")

    servidor.registrar_usuario("Aldana", "aldana@mail.com", "123")
    servidor.registrar_usuario("Juan", "juan@mail.com", "abc")

    usuario1, _ = servidor.iniciar_sesion("aldana@mail.com", "123")
    usuario2, _ = servidor.iniciar_sesion("juan@mail.com", "abc")

    # Crear carpetas y filtros automáticos
    usuario1.crear_carpeta("Trabajo")
    usuario1.agregar_filtro("Proyecto", "Trabajo")

    # Envío de mensajes con prioridad

    # Mensaje urgente
    servidor.enviar_mensaje(
        usuario2,
        "aldana@mail.com",
        "URGENTE: Proyecto final",
        "Necesito el archivo Miércoles.",
        prioridad=1
    )

    # Mensaje normal
    servidor.enviar_mensaje(
        usuario2,
        "aldana@mail.com",
        "Consulta",
        "¿Vamos a entregar mañana?",
        prioridad=2
    )

    # Procesar urgentes y mostrar resultados
    print("=== Urgentes en cola ANTES de procesar ===")
    print(usuario1.ver_urgentes_pendientes())

    usuario1.procesar_urgentes()

    print("\n=== Mensajes en Recibidos (ordenados por fecha) ===")
    for m in usuario1.listar_inbox():
        print(m)

    # Mover y borrar mensajes
    resultado = usuario1.buscar_mensajes(asunto="Consulta")
    if resultado:
        mensaje_a_borrar = resultado[0]
        usuario1.borrar_mensaje(mensaje_a_borrar, usuario1.obtener_carpeta("Recibidos"))

    print("\n=== Papelera ===")
    for m in usuario1.obtener_carpeta("Papelera").listar_mensajes():
        print(m)

    # Mostrar red de servidores y ruta BFS
    print("\n=== Grafo interno del servidor (para BFS) ===")
    print(servidor.mostrar_red())

    print("\nRuta BFS en este servidor (único nodo):")
    print(servidor.ruta_BFS("ServidorCentral", "ServidorCentral"))

if __name__ == "__main__":
    main()