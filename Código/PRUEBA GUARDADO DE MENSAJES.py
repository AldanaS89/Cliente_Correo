# main.py modificado
import pickle
import os
from servidorcorreo import ServidorCorreo
from validaciones import registro_valido, login
from menu import menu_sesion

ARCHIVO_DATOS = "datos_servidor.pkl"

def guardar_datos(servidor):
    """Guarda el objeto servidor completo en un archivo."""
    with open(ARCHIVO_DATOS, "wb") as f:
        pickle.dump(servidor, f)
    print("\n[Sistema] Datos guardados exitosamente.")

def cargar_datos():
    """Intenta cargar el servidor desde el archivo. Si no existe, crea uno nuevo."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "rb") as f:
                servidor = pickle.load(f)
            print("\n[Sistema] Datos cargados correctamente.")
            return servidor
        except Exception as e:
            print(f"[Sistema] Error al cargar datos: {e}. Se creará uno nuevo.")
    
    # Si no hay archivo, creamos el servidor y los usuarios de prueba iniciales
    print("\n[Sistema] Iniciando servidor nuevo...")
    servidor = ServidorCorreo("Gmail")
    servidor.registrar_usuario("Admin", "admin@mail.com", "1234")
    servidor.registrar_usuario("Aldana", "aldana@mail.com", "1234")
    return servidor

if __name__ == "__main__":
    # 1. Cargar datos al inicio
    servidor = cargar_datos()
    
    print("\n--- SIMULADOR DE CORREO ---")
    while True:
        print("\n1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        accion = input("Opción: ").strip()

        if accion == "1":
            usuario_actual = login(servidor)
            if usuario_actual:
                menu_sesion(usuario_actual, servidor)
                # Opcional: Guardar cada vez que alguien cierra sesión
                guardar_datos(servidor) 
        
        elif accion == "2":
            registro_valido(servidor)
            # Guardamos después de un registro exitoso
            guardar_datos(servidor)
        
        elif accion == "3":
            # 2. Guardar datos al salir
            guardar_datos(servidor)
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")