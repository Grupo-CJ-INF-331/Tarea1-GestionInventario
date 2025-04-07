# Tarea1-GestionInventario

# Especificación de Requerimientos del Sistema de Gestión de Inventario

## 1. Introducción

Este documento describe los requerimientos funcionales y no funcionales del sistema de gestión de inventario. El sistema tiene como objetivo principal permitir el control eficiente de productos, stock y reportes, con acceso restringido a través de autenticación segura.

Los requisitos entregados en el contexto de la tarea estaban incompletos, por lo que en este documento nos encargaremos de describir los criterios de aceptacion de cada requerimiento para eliminar ambiguedades.

Adicionalmente comprobaremos que el programa cumpla cada requerimiento por medio de pruebas, estas pruebas verificara que el funcionamiento de la aplicacion cumpla con los requerimientos.

Evidencia de flujo de trabajo son los requerimientos documentados.

El desarrollo de este producto no requiere de un roadmap para detallar tiempos, esfuerzos y recursos.

La estrategia de pruebas a implementar es son las de pruebas unitarias, en este repositorio se encuentra un archivo excel con mas detalles. Los casos de prueba fueron ejecutados por el equipo desarrollador.

El paradigma utilizado para administrar los codigos es el de Trunk based development, es facil de entender e implementar, todos los desarrolladores pueden adaptarse facilmente. Todos los cambios se hacen desde una rama y se hace el merge al trunk a traves de un peer review.

---

## 2. Requerimientos Funcionales

### 2.1. Gestión de Productos (CRUD)

**Descripción:**  
El sistema debe permitir a los usuarios autenticados crear, consultar, modificar y eliminar productos en el inventario.

**Atributos del producto:**

- `nombre` (string)
- `descripción` (string)
- `cantidad` (entero)
- `precio` (decimal)
- `categoría` (enum): Ej. Electrónica, Ropa, Alimentos, etc.

**Operaciones disponibles:**

| Operación  | Descripción                                        |
|------------|----------------------------------------------------|
| Crear      | Registrar un nuevo producto.                       |
| Consultar  | Visualizar productos registrados.                  |
| Actualizar | Modificar atributos de un producto existente.      |
| Eliminar   | Remover un producto del sistema.                   |

**Criterios de Aceptación:**

- **Crear:**
  - El sistema debe permitir crear un producto si todos los campos requeridos están completos y válidos.
  - El sistema no debe aceptar valores negativos en cantidad o precio.

- **Consultar:**
  - El sistema debe listar todos los productos disponibles con sus atributos visibles.
  

- **Actualizar:**
  - El sistema debe permitir modificar todos los atributos del producto excepto su ID.
  - El sistema debe validar que los nuevos valores cumplan con las reglas de formato y tipo de dato.
  - Al guardar los cambios, debe mostrarse una notificación de éxito.

- **Eliminar:**
  - El sistema debe solicitar confirmación antes de eliminar un producto.
  - Si el producto se elimina correctamente, debe desaparecer del listado.
  - No debe ser posible eliminar un producto inexistente.

---

### 2.2. Control de Stock

**Descripción:**  
Permite modificar la cantidad de productos disponibles mediante ingreso o salida de unidades.

**Tipos de movimiento:**

- **Editar cantidad:** Incrementa o disminuye la cantidad por recepción o compra.


**Criterios de Aceptación:**

- **Editar cantidad:**
  - El sistema debe permitir ingresar unidades adicionales a un producto existente.
  - La cantidad ingresada debe ser un número entero positivo.
  - El movimiento debe registrarse correctamente en el historial con fecha y cantidad.
  - No debe permitir registrar una salida que deje el stock negativo.

---

### 2.3. Filtrado y Búsqueda

**Descripción:**  
El sistema debe permitir búsquedas de productos mediante:

- Nombre (búsqueda parcial o exacta)
- Categoría
- Descripción

**Criterios de Aceptación:**

- El sistema debe permitir búsquedas por nombre (exacta o parcial).
- Al buscar por categoría, debe mostrarse solo los productos de dicha categoría.


---

### 2.4. Generación de Reportes

**Descripción:**  
El sistema debe generar reportes visuales y exportables sobre el estado del inventario.

**Reportes requeridos:**

| Reporte                    | Descripción                                                       |
|----------------------------|-------------------------------------------------------------------|
| Resumen general            | Total de productos y unidades en stock.                          |
| Valor del inventario       | Suma de (cantidad × precio_unitario) de todos los productos.     |


**Formatos de salida:**

- Visual en interfaz

**Criterios de Aceptación:**

- **Resumen general:**
  - El sistema debe mostrar la cantidad total de productos y unidades disponibles.
  - Debe reflejar el stock actualizado en tiempo real.

- **Valor del inventario:**
  - El cálculo debe ser exacto: `cantidad * precio_unitario` por producto, sumado.



---

### 2.5. Autenticación y Control de Acceso

**Descripción:**  
Sistema de autenticación con credenciales y control de roles.

**Requisitos:**

- Inicio y cierre de sesión
- Cifrado de contraseñas (bcrypt)

**Criterios de Aceptación:**

- **Inicio de sesión:**
  - El sistema debe permitir iniciar sesión solo con credenciales válidas.
  - Si las credenciales son incorrectas, debe mostrarse un mensaje de error sin revelar cuál campo falló.
  

- **Seguridad:**
  - Las contraseñas deben estar cifradas con bcrypt, Argon2 o equivalente.
  - No debe ser posible recuperar contraseñas desde la base de datos.
  

---



## 3. Requerimientos No Funcionales

### 3.1. Seguridad

- Cifrado de contraseñas con hash seguro


---

### 3.2. Usabilidad

- Interfaz clara e intuitiva
- Validaciones en tiempo real
- Compatible con navegadores modernos
- Soporte básico de accesibilidad (uso de teclado, contraste, etiquetas)
---



**Fin del documento**
