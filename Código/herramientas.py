# Herramientas para manejar enteros en el menú

def pedir_entero(mensaje, minimo=None, maximo=None):
    # Pide un entero válido, opcionalmente dentro de un rango.
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            return None
        try:
            valor = int(entrada)
            if minimo is not None and valor < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"El valor debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Debes ingresar un número entero.")
