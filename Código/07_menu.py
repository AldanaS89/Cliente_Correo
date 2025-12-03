from herramientas import pedir_entero

# =====================================================
#   MENU AUXILIAR: ACCIONES TRAS BÚSQUEDA
# =====================================================
def acciones_resultado_busqueda(usuario, mensaje):
    while True:
        print("\n" + "-"*40)
        print(f"MENSAJE SELECCIONADO: {mensaje.resumen()}")
        print("-"*40)
        print(" [1] Leer contenido")
        print(" [2] Mover mensaje")
        print(" [3] Eliminar mensaje (Enviar a Papelera)")
        print(" [0] Volver a la lista de resultados")

        opcion = input("\nAcción: ").strip()

        if opcion == "1":
            print("\n" + mensaje.mostrar_detalle())
            input("Presiona Enter para volver...")

        elif opcion == "2":
            print("\n¿A dónde moverlo?")
            dests_raw = usuario.obtener_arbol_destinos() 
            
            # --- Excluir 'Enviados' ---
            destinos_validos = []
            for nombre_visual, obj_carpeta in dests_raw:
                if obj_carpeta.nombre != "Enviados":
                    destinos_validos.append((nombre_visual, obj_carpeta))

            if not destinos_validos:
                print("No hay carpetas destino válidas.")
                continue

            # Mostrar solo las carpetas permitidas
            for i, (nombre_visual, obj_carpeta) in enumerate(destinos_validos):
                print(f"[{i}] {nombre_visual}")

            # Elegir usando el índice de la lista FILTRADA
            idx = pedir_entero("Elige destino: ", 0, len(destinos_validos)-1)
            carpeta_destino = destinos_validos[idx][1]

            # Lógica de movimiento
            movido = False
            if usuario.recibidos.mover_mensaje(mensaje, carpeta_destino):
                movido = True
            elif usuario.enviados.mover_mensaje(mensaje, carpeta_destino):
                movido = True
            elif usuario.papelera.mover_mensaje(mensaje, carpeta_destino):
                movido = True
            
            if movido:
                print("Mensaje movido correctamente.")
                return 
            else:
                print("Error: No se pudo mover (quizás el mensaje ya no existe).")

        elif opcion == "3":
            confirmar = input("¿Enviar a papelera? (s/n): ").lower()
            if confirmar == "s":
                movido = False
                if usuario.recibidos.mover_mensaje(mensaje, usuario.papelera):
                    movido = True
                elif usuario.enviados.mover_mensaje(mensaje, usuario.papelera):
                    movido = True
                
                if movido:
                    print("Mensaje enviado a la Papelera.")
                    return 
                else:
                    print("El mensaje ya está en la papelera o no se pudo mover.")
        
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")

# =====================================================
#   FUNCIÓN PARA NAVEGAR DENTRO DE UNA CARPETA
# =====================================================
def navegar_carpeta(usuario, carpeta_actual):
    while True:
        es_enviados = (carpeta_actual.nombre == "Enviados")
        es_papelera = (carpeta_actual.nombre == "Papelera")
        
        root = carpeta_actual
        while root._padre is not None:
            root = root._padre
        
        estoy_en_papelera = (root.nombre == "Papelera") or es_papelera

        print("\n" + "="*60)
        print(f"ESTÁS EN: {carpeta_actual.nombre}")
        if carpeta_actual._padre:
            print(f"   (Dentro de: {carpeta_actual._padre.nombre})")
        print("="*60)

        # MOSTRAR CONTENIDO
        subcarpetas = carpeta_actual.obtener_subcarpetas()
        lista_sub = list(subcarpetas.keys())
        mensajes = carpeta_actual.obtener_mensajes()

        if not es_enviados:
            print(f"\n--- SUBCARPETAS ({len(lista_sub)}) ---")
            if not lista_sub:
                print("  (vacío)")
            for i, nombre in enumerate(lista_sub):
                print(f"  [Carpeta {i}] {nombre}")

        print(f"\n--- MENSAJES ({len(mensajes)}) ---")
        if not mensajes:
            print("  (vacío)")
        for i, msg in enumerate(mensajes):
            # MODO VISUALIZACION: Enviados vs Recibidos
            modo_visual = "enviados" if es_enviados else "recibidos"
            print(f"  [Mensaje {i}] {msg.resumen(modo_visual)}")

        # MENU DE ACCIONES
        print("\n--- ACCIONES ---")
        print(" [1] Leer mensaje")
        print(" [2] Mover mensaje")
        
        if not estoy_en_papelera:
            print(" [3] Eliminar mensaje")

        if not es_enviados: 
            print(" [4] Ingresar a subcarpeta") 

        if not es_enviados and not estoy_en_papelera:
            print(" [5] Crear subcarpeta")
            print(" [6] Mover subcarpeta")
            print(" [7] Eliminar subcarpeta (Enviar a Papelera)")
        
        print(" [0] Volver al menú anterior")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1": 
            if not mensajes:
                print("No hay mensajes.")
                continue
            idx = pedir_entero("Número de mensaje: ", 0, len(mensajes)-1)
            print("\n" + mensajes[idx].mostrar_detalle())
            input("Presiona Enter para continuar...")

        elif opcion == "2":
            if not mensajes:
                print("No hay mensajes para mover.")
                continue
            idx = pedir_entero("Número de mensaje a mover: ", 0, len(mensajes)-1)
            msg = mensajes[idx]

            print("\n¿A dónde quieres moverlo?")
            dests_raw = usuario.obtener_arbol_destinos()
            destinos_validos = []

            for nombre_visual, obj_carpeta in dests_raw:
                if obj_carpeta.nombre == "Enviados": continue
                if obj_carpeta is carpeta_actual: continue
                destinos_validos.append((nombre_visual, obj_carpeta))
            
            if not destinos_validos:
                print("No hay destinos válidos.")
                continue

            for i, (n_v, obj_c) in enumerate(destinos_validos):
                print(f"  [{i}] {n_v}")
            
            d_idx = pedir_entero("Elige carpeta destino: ", 0, len(destinos_validos)-1)
            carpeta_destino = destinos_validos[d_idx][1]

            if carpeta_actual.mover_mensaje(msg, carpeta_destino):
                print("Mensaje movido/recuperado.")
            else:
                print("Error al mover.")

        elif opcion == "3": 
            if estoy_en_papelera:
                print("No puedes borrar mensajes de la Papelera manualmente.")
                continue
            
            if not mensajes:
                print("No hay mensajes.")
                continue
            
            idx = pedir_entero("Número de mensaje a eliminar: ", 0, len(mensajes)-1)
            msg = carpeta_actual.eliminar_mensaje(idx)
            usuario.papelera.agregar_mensaje(msg)
            print("Mensaje enviado a la Papelera.")

        elif opcion == "4":
            if es_enviados:
                print("Acción no válida.")
                continue
            if not lista_sub:
                print("No hay subcarpetas.")
                continue
            idx = pedir_entero("Número de carpeta para entrar: ", 0, len(lista_sub)-1)
            navegar_carpeta(usuario, subcarpetas[lista_sub[idx]])

        elif opcion in ["5", "6", "7"]:
            if es_enviados or estoy_en_papelera:
                print("Acción no permitida aquí.")
                continue

            if opcion == "5":
                nombre = input("Nombre de la nueva carpeta: ").strip()
                if nombre:
                    ok, txt = carpeta_actual.crear_subcarpeta(nombre)
                    print(f"Sistema: {txt}")

            elif opcion == "6":
                if not lista_sub:
                    print("No hay carpetas.")
                    continue
                idx = pedir_entero("Número de carpeta a mover: ", 0, len(lista_sub)-1)
                nombre_mover = lista_sub[idx]

                print(f"\n--- Selecciona el DESTINO para '{nombre_mover}' ---")
                dests_raw = usuario.obtener_arbol_destinos()
                
                destinos_carpeta = []
                for n_v, obj_c in dests_raw:
                    if obj_c.nombre in ["Enviados", "Papelera"]: continue
                    destinos_carpeta.append((n_v, obj_c))

                for i, (n_v, obj_c) in enumerate(destinos_carpeta):
                    print(f"[{i}] {n_v}")

                sel = pedir_entero("Elige destino: ", 0, len(destinos_carpeta)-1)
                carpeta_destino = destinos_carpeta[sel][1] 

                ok, txt = carpeta_actual.mover_subcarpeta(nombre_mover, carpeta_destino)
                print(f"Sistema: {txt}")

            elif opcion == "7":
                if not lista_sub:
                    print("No hay carpetas.")
                    continue
                idx = pedir_entero("Número de carpeta a borrar: ", 0, len(lista_sub)-1)
                nombre_borrar = lista_sub[idx]
                
                print(f"¿Enviar '{nombre_borrar}' a la Papelera? (s/n)")
                if input(": ").lower() == "s":
                    ok, txt = carpeta_actual.mover_subcarpeta(nombre_borrar, usuario.papelera)
                    if ok: print("Carpeta enviada a la Papelera.")
                    else: print(f"Error: {txt}")

        elif opcion == "0":
            return
        else:
            print("Opción inválida.")

# =====================================================
#   MENÚ PRINCIPAL DE SESIÓN
# =====================================================
def menu_sesion(usuario, servidor):
    while True:
        print("\n" + "="*50)
        print(f"BIENVENIDO, {usuario.nombre.upper()}")
        print("="*50)
        print("1. RECIBIDOS")
        print("2. ENVIADOS")
        print("3. PAPELERA")
        print("4. ENVIAR MENSAJE")
        print("5. BUSCAR MENSAJE")
        print("6. CREAR FILTRO")
        print("7. CERRAR SESIÓN")
        print("="*50)

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            navegar_carpeta(usuario, usuario.recibidos)

        elif opcion == "2":
            navegar_carpeta(usuario, usuario.enviados)

        elif opcion == "3":
            usuario.limpiar_papelera()
            navegar_carpeta(usuario, usuario.papelera)

        elif opcion == "4":
            print("\n--- NUEVO MENSAJE ---")
            destino = input("Para (correo): ").strip()
            asunto = input("Asunto: ").strip()
            cuerpo = input("Mensaje: ").strip()
            prioridad = pedir_entero("Prioridad (1=Urgente / 2=Normal): ", 1, 2)

            exito, msg_txt = servidor.enviar_mensaje(usuario, destino, asunto, cuerpo, prioridad)
            print(f"\n>> {msg_txt}")

        elif opcion == "5":
            texto = input("\nBuscar (Asunto o Remitente): ").strip()
            if not texto: continue

            resultados = usuario.buscar_mensajes(texto)

            if not resultados:
                print("No se encontraron coincidencias.")
                continue

            while True:
                print(f"\nRESULTADOS DE: '{texto}' ({len(resultados)})")
                print("No. | Resumen")
                print("-" * 40)
                for i, m in enumerate(resultados):
                    print(f"[{i}] {m.resumen()}")
                print("-" * 40)
                
                seleccion = input("Opción (Nº mensaje o 'v' volver): ").strip().lower()
                if seleccion == 'v': break 

                if seleccion.isdigit():
                    idx = int(seleccion)
                    if 0 <= idx < len(resultados):
                        acciones_resultado_busqueda(usuario, resultados[idx])
                    else:
                        print("Número fuera de rango.")
                else:
                    print("Opción inválida.")

        elif opcion == "6":
            print("\n--- CREAR FILTRO AUTOMÁTICO ---")
            email_filtro = input("Email del remitente a filtrar: ").strip()
            
            if not email_filtro:
                print("Cancelado: Debes escribir un email.")
                continue

            print(f"\n¿Dónde guardar los mensajes de '{email_filtro}'?")
            print(" [1] Crear una CARPETA NUEVA ahora mismo")
            print(" [2] Elegir una carpeta EXISTENTE")
            
            decision = input("Opción: ").strip()
            carpeta_elegida = None

            if decision == "1":
                nombre_nueva = input("Nombre de la nueva carpeta: ").strip()
                if nombre_nueva:
                    # Intentamos crearla dentro de 'Recibidos'
                    exito, msg = usuario.recibidos.crear_subcarpeta(nombre_nueva)
                    print(f"Sistema: {msg}")
                    
                    if exito:
                        carpeta_elegida = usuario.recibidos.obtener_subcarpeta(nombre_nueva)
                    else:
                        # Si falló (ej: ya existía), preguntamos
                        print("¿Deseas usar la carpeta existente con ese nombre? (s/n)")
                        if input(": ").lower() == "s":
                            carpeta_elegida = usuario.recibidos.obtener_subcarpeta(nombre_nueva)
            
            elif decision == "2":
                destinos = usuario.obtener_arbol_destinos()
                
                opciones_validas = []
                print("\nCarpetas disponibles:")
                for i, (nombre_visual, obj_carpeta) in enumerate(destinos):
                    if obj_carpeta.nombre not in ["Enviados", "Papelera"]:
                        print(f"  [{len(opciones_validas)}] {nombre_visual}")
                        opciones_validas.append(obj_carpeta)
                
                if opciones_validas:
                    idx = pedir_entero("\nElige el número de carpeta: ", 0, len(opciones_validas)-1)
                    carpeta_elegida = opciones_validas[idx]
                else:
                    print("No hay carpetas válidas creadas.")

            if carpeta_elegida:
                exito_filtro, txt_filtro = usuario.agregar_filtro(email_filtro, carpeta_elegida)
                print(f"\n>> {txt_filtro}")
            else:
                print("\nOperación cancelada o carpeta inválida.")

            input("Presiona Enter para continuar...")

        elif opcion == "7":
            print("Cerrando sesión...")
            break
        else:
            print("Opción incorrecta.")
