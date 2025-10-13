# Proyecto: Cliente de correo electrónico.

## Descripción general: 
El objetivo es diseñar e implementar, en **Python**, un sistema orientado a objetos que modele un cliente de correo electrónico, permitiendo la gestión de **usuarios, mensajes, carpetas, filtros y operaciones típicas** de un entorno de email.

## Entrega 1: Modelado de clases y encapsulamiento.
Se definieron las clases principales:  
- **Mensaje:** Representa un correo electrónico con remitente, destinatario, asunto y contenido.  
- **Carpeta:** Almacena y organiza los mensajes del usuario.  
- **Usuario:** Contiene los datos del usuario y gestiona sus carpetas.  
- **ServidorCorreo:** Administra a los usuarios y la comunicación entre ellos.  
Cada clase utiliza **atributos encapsulados** y **propiedades** para garantizar un acceso controlado a los datos.  
También se implementaron operaciones básicas de envío, recepción y listado de mensajes.

## Entrega 2: Estructuras de Datos y Recursividad.
Se incorporaron los conceptos de **árbol general** modificando la clase *Carpeta* de manera tal que acepte *Subcarpetas* formando así una **estructura recursiva tipo árbol**.  
Cada carpeta puede tener mensajes y también otras carpetas, permitiendo de esta manera organizar la información.  

Además se agregaron métodos que permiten:  
- **Buscar mensajes recursivamente:** Ya sea por asunto o por remitente.
- **Mover mensajes:** Entre carpetas, aplicando la misma estructura recursiva.

**Estudiante:** Aldana Benavent.  
**Materia:** Estructura de Datos.
