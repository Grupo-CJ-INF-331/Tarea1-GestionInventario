import sqlite3
import bcrypt
import logging

# Configuración de logs
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def conectar_bd():
    return sqlite3.connect("inventario.db")


def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
                        precio REAL NOT NULL CHECK (precio >= 0),
                        categoria TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def registrar_usuario(username, password):
    if not username or not password:
        print("El nombre de usuario y la contraseña no pueden estar vacíos.")
        return
    conn = conectar_bd()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        logging.info(f"Usuario {username} registrado con éxito.")
        print("Usuario registrado con éxito.")
    except sqlite3.IntegrityError:
        logging.warning(f"Intento de registrar usuario duplicado: {username}")
        print("El usuario ya existe.")
    finally:
        conn.close()


def autenticar_usuario():
    for intento in range(3):
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user[0]):
            logging.info(f"Usuario {username} autenticado con éxito.")
            print("Autenticación exitosa.")
            return True
        logging.warning(f"Fallo de autenticación para usuario: {username}")
        print("Credenciales incorrectas. Intente de nuevo.")
    print("Demasiados intentos fallidos.")
    return False


def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    if cantidad < 0 or precio < 0:
        print("Cantidad y precio deben ser valores positivos.")
        return
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                       (nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        logging.info(f"Producto {nombre} agregado con éxito.")
        print("Producto agregado correctamente.")
    except sqlite3.Error as e:
        print("Error al agregar producto:", e)
        logging.error(f"Error al agregar producto: {e}")
    finally:
        conn.close()


def listar_productos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos


def buscar_productos_por_filtro(campo, valor):
    campos_validos = ["nombre", "descripcion", "categoria"]
    if campo not in campos_validos:
        print(f"Campo inválido. Use uno de: {', '.join(campos_validos)}")
        return []
    conn = conectar_bd()
    cursor = conn.cursor()
    consulta = f"SELECT * FROM productos WHERE {campo} LIKE ?"
    cursor.execute(consulta, (f"%{valor}%",))
    productos = cursor.fetchall()
    conn.close()
    return productos


def actualizar_stock(id_producto, nueva_cantidad):
    if nueva_cantidad < 0:
        print("La cantidad no puede ser negativa.")
        return
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM productos WHERE id = ?", (id_producto,))
    if cursor.fetchone() is None:
        print("Producto no encontrado.")
        conn.close()
        return
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
    conn.commit()
    conn.close()
    logging.info(f"Stock del producto {id_producto} actualizado a {nueva_cantidad}.")
    print("Stock actualizado correctamente.")


def eliminar_producto(id_producto):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM productos WHERE id = ?", (id_producto,))
    if cursor.fetchone() is None:
        print("Producto no encontrado.")
        conn.close()
        return
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()
    logging.info(f"Producto {id_producto} eliminado.")
    print("Producto eliminado correctamente.")


def generar_reporte():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(cantidad), SUM(cantidad * precio) FROM productos")
    total_productos, valor_total = cursor.fetchone()
    total_productos = total_productos or 0
    valor_total = valor_total or 0.0
    cursor.execute("SELECT * FROM productos WHERE cantidad = 0")
    agotados = cursor.fetchall()
    conn.close()
    return total_productos, valor_total, agotados


def menu():
    while True:
        print("\nSistema de Gestión de Inventario")
        print("1. Agregar usuario")
        print("2. Agregar producto")
        print("3. Listar productos")
        print("4. Buscar productos")
        print("5. Actualizar stock")
        print("6. Eliminar producto")
        print("7. Generar reporte")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            username = input("Ingrese nuevo nombre de usuario: ")
            password = input("Ingrese contraseña: ")
            registrar_usuario(username, password)

        elif opcion == "2":
            try:
                nombre = input("Nombre del producto: ")
                descripcion = input("Descripción: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                categoria = input("Categoría: ")
                agregar_producto(nombre, descripcion, cantidad, precio, categoria)
            except ValueError:
                print("Error: asegúrese de ingresar números válidos para cantidad y precio.")

        elif opcion == "3":
            productos = listar_productos()
            if productos:
                for p in productos:
                    print(p)
            else:
                print("No hay productos registrados.")

        elif opcion == "4":
            campo = input("Ingrese el campo a buscar (nombre, descripcion, categoria): ")
            valor = input("Ingrese el valor a buscar: ")
            productos = buscar_productos_por_filtro(campo, valor)
            if productos:
                for p in productos:
                    print(p)
            else:
                print("No se encontraron productos.")

        elif opcion == "5":
            try:
                id_producto = int(input("ID del producto: "))
                nueva_cantidad = int(input("Nueva cantidad: "))
                actualizar_stock(id_producto, nueva_cantidad)
            except ValueError:
                print("ID y cantidad deben ser números enteros.")

        elif opcion == "6":
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                eliminar_producto(id_producto)
            except ValueError:
                print("Debe ingresar un ID válido.")

        elif opcion == "7":
            total, valor, agotados = generar_reporte()
            print(f"Total de productos en stock: {total}")
            print(f"Valor total del inventario: ${valor:.2f}")
            if agotados:
                print("Productos agotados:")
                for p in agotados:
                    print(p)
            else:
                print("No hay productos agotados.")

        elif opcion == "8":
            print("Saliendo...")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    inicializar_bd()
    if autenticar_usuario():
        menu()
