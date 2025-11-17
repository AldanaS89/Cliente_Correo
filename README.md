# Proyecto: Cliente de correo electrónico.  
**Autora:** Aldana Benavent  
**Materia:** Estructura de Datos  
**Grupo:** 38

## Descripción general: 
El objetivo de este proyecto es diseñar e implementar, en **Python**, un sistema orientado a objetos que modele un cliente de correo electrónico, permitiendo la gestión de **usuarios, mensajes, carpetas, filtros y operaciones típicas** de un entorno de email.  
El sistema se desarrolló utilizando **encapsulamiento**, **modularización**, **estructuras de datos** (árbol, grafos, heap), **algoritmos de búsqueda** (BFS y búsquedas recursivas) y **cola de prioridad** para mensajes urgentes.  
La finalidad fue modelar un sistema simple priorizando la **organización, eficiencia y escalabilidad** del código.  

## Estructura del proyecto:  
Para mejorar la organización y facilitar el mantenimiento del código, el proyecto fue **modularizado** en distintos archivos, cada uno con una responsabilidad específica:    

Cliente Correo/   
  mensaje.py               → Define la clase Mensaje  
  carpeta.py               → Implementa la clase Carpeta, con subcarpetas (estructura de árbol)  
  usuario.py               → Gestiona usuarios y sus carpetas  
  servidorcorreo.py        → Administra el envío y recepción de correos entre usuarios (grafo + BFS)  
  main.py                  → Archivo principal con pruebas e integración del sistema
  
## Entrega 1: Modelado de clases y encapsulamiento.
Se definieron las clases principales:  
- **Mensaje:** Representa un correo electrónico con remitente, destinatario, asunto y contenido.  
- **Carpeta:** Almacena y organiza los mensajes del usuario.  
- **Usuario:** Contiene los datos del usuario y gestiona sus carpetas.  
- **ServidorCorreo:** Administra a los usuarios y la comunicación entre ellos.  
Cada clase utiliza **atributos encapsulados** y **propiedades** para garantizar un acceso controlado a los datos.  
También se implementaron operaciones básicas de **envío**, **recepción** y **listado de mensajes**.

## Entrega 2: Estructuras de Datos y Recursividad.
Se incorporaron los conceptos de **árbol general** modificando la clase *Carpeta* de manera tal que acepte *Subcarpetas* formando así una **estructura recursiva tipo árbol**.  
Cada carpeta puede tener mensajes y también otras carpetas, permitiendo de esta manera organizar la información.  

Además se agregaron métodos que permiten:  
- **Buscar mensajes recursivamente:** Ya sea por asunto o por remitente.
- **Mover mensajes:** Entre carpetas, utilizando recursividad.

## Entrega 3: Algoritmos y Funcionalidades Avanzadas.  
El sistema integra diversas **estructuras de datos y algoritmos** para optimizar su funcionamiento:  
- **Filtros automáticos:** Utilizan listas y diccionarios (Complejidad O(n))
- **Cola de prioridad:** Implementada con un **Min-Heap** para mensajes urgentes (Complejidad O(log k))
- **Red de servidores:** Representada como un **grafo**, con envío de mensajes mediante **BFS** (Complejidad O(V+E))
- **Jerarquía de carpetas:** Estructurada como un **árbol** con búsquedas recursivas mediante **DFS** (Complejidad O(n))

Cada algoritmo y estructura fue elegido por su **eficiencia y adecuación al problema**, logrando un modelo que refleja con precisión el funcionamiento de un entorno real de correo electrónico.  

  ## Entrega 4: Integración, pruebas y decisiones finales.  
  **Decisiones principales:**  
  - **Modularización:**
    Para que el código sea más simple de leer y fácil de mantener es que se tomó la decisión de separar cada clase en un archivo.
  - **Mensajes urgentes:**
    Para manejar las prioridades se utilizó un *heapq* ya que esto permite procesar los urgentes antes de los normales evitando de esta manera recorrer toda la lista.
  - **Carpetas como árbol:**
    Además de tener una estructura similar a la de un correo real, el árbol facilita las búsquedas recursivas
  - **Servidor como grafo:**
    Se implementó para demostrar uso de grafos y BFS, aunque el proyecto use un solo servidor.
  - **Ordenamiento por fecha:**
    Para mejor la experiencia de lectura los mensajes se insertan automáticamente del más nuevo al más antiguo sin modificar los mensajes urgentes.

**Ejecución del proyecto:**  
Para correr el código fue creado el archivo **main.py**. El mismo muestra cómo funciona el sistema:  
1. Se crea un servidor.
2. Se registran usuarios.
3. Se crean carpetas.
4. Se agregan filtros.
5. Se envían mensajes normales y urgentes.
6. Se procesan urgentes.
7. Se muestran inbox ordenados por fecha.
8. Se mueve y borra un mensaje.
9. Se muestra la red del servidor y una ruta BFS.
