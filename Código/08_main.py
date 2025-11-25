# Archivo principal del proyecto: Cliente de correo electrónico
# Autora: Aldana Benavent - Grupo 38
# Este archivo muestra cómo se integran los módulos del proyecto y permite realizar pruebas simples del sistema.

from servidorcorreo import ServidorCorreo
from validaciones import registro_valido, login
from menu import menu_sesion # <--- Importamos el menú

if __name__ == "__main__":
    servidor = ServidorCorreo("Gmail")
    
    # Usuarios de prueba
    servidor.registrar_usuario("Admin", "admin@mail.com", "1234")
    servidor.registrar_usuario("Aldana", "aldana@mail.com", "1234")

    print("\n--- SIMULADOR DE CORREO ---")
    while True:
        print("\n1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        accion = input("Opción: ").strip()

        if accion == "1":
            usuario_actual = login(servidor)
            if usuario_actual:
                # Aquí derivamos el control al archivo menú
                menu_sesion(usuario_actual, servidor)
        
        elif accion == "2":
            registro_valido(servidor)
        
        elif accion == "3":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")

