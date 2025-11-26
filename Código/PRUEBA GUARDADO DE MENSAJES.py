import pickle
import os
from servidorcorreo import ServidorCorreo
from validaciones import registro_valido, login
from menu import menu_sesion

# Nombre del archivo donde se guardarán los datos
ARCHIVO_DATOS = "datos_servidor.pkl"

def guardar_datos(servidor):
    """Guarda el estado completo del servidor en un archivo."""
    try:
        with open(ARCHIVO_DATOS, "wb") as f:
            pickle.dump(servidor, f)
        print("\n[Sistema] Datos guardados exitosamente.")
    except Exception as e:
        print(f"\n[Error] No se pudieron guardar los datos: {e}")

def cargar_datos():
    """Carga el servidor desde el archivo o crea uno nuevo con datos de prueba."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "rb") as f:
                servidor = pickle.load(f)
            print("\n[Sistema] Datos previos cargados correctamente.")
            return servidor
        except Exception as e:
            print(f"[Sistema] Archivo dañado ({e}). Iniciando servidor nuevo...")
    
    # Si no hay archivo o falló la carga, creamos datos desde cero
    print("\n[Sistema] Iniciando servidor nuevo...")
    servidor = ServidorCorreo("Gmail")
    
    # Usuarios de prueba iniciales
    print("Creando usuarios por defecto (Admin, Aldana)...")
    servidor.registrar_usuario("Admin", "admin@mail.com", "1234")
    servidor.registrar_usuario("Aldana", "aldana@mail.com", "1234")
    
    return servidor

if __name__ == "__main__":
    # 1. Cargar datos al iniciar el programa
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
                # Entramos al menú principal de la sesión
                menu_sesion(usuario_actual, servidor)
                
                # Al cerrar sesión, guardamos por seguridad
                guardar_datos(servidor)
        
        elif accion == "2":
            registro_valido(servidor)
            # Al registrar un usuario nuevo, guardamos inmediatamente
            guardar_datos(servidor)
        
        elif accion == "3":
            # Guardado final al salir
            guardar_datos(servidor)
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")
