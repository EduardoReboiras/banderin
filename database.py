import mysql.connector
from mysql.connector import Error

class LibreriaBD:
    def __init__(self):
        # Configura aquí tus datos de conexión local
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '', # Pon tu contraseña de MySQL
            'database': 'libreria_banderin'
        }

    def obtener_conexion(self):
        """Establece y retorna la conexión con la base de datos."""
        try:
            conexion = mysql.connector.connect(**self.config)
            return conexion
        except Error as e:
            print(f"\n[Error de Conexión]: {e}")
            return None

    def buscar_producto_por_nombre(self, nombre_buscar):
        """Busca productos por coincidencia de nombre."""
        conexion = self.obtener_conexion()
        if not conexion: return []

        resultados = []
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT id_producto, nombre, precio, stock_actual FROM productos WHERE nombre LIKE %s"
            cursor.execute(query, (f"%{nombre_buscar}%",))
            resultados = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Error al buscar: {e}")
        finally:
            conexion.close()
        return resultados

    def verificar_stock_critico(self):
        """Trae los productos cuyo stock actual es menor o igual al mínimo."""
        conexion = self.obtener_conexion()
        if not conexion: return []

        resultados = []
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT nombre, stock_actual, stock_minimo FROM productos WHERE stock_actual <= stock_minimo"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Error al verificar stock: {e}")
        finally:
            conexion.close()
        return resultados

    def registrar_cliente(self, nombre, apellido, email, password):
        """Inserta un nuevo cliente en la base de datos."""
        conexion = self.obtener_conexion()
        if not conexion: return False

        exito = False
        try:
            cursor = conexion.cursor()
            query = """INSERT INTO clientes (nombre, apellido, email, password_hash) 
                       VALUES (%s, %s, %s, %s)"""
            # NOTA: En un entorno real, 'password' debería encriptarse antes de guardarse
            cursor.execute(query, (nombre, apellido, email, password))
            conexion.commit() # Confirmamos los cambios en la BD
            exito = True
            cursor.close()
        except Error as e:
            print(f"Error al registrar cliente: {e}")
        finally:
            conexion.close()
        return exito
    
    def realizar_pedido(self, id_cliente, lista_productos):
        """
        Registra un pedido completo y descuenta el stock.
        'lista_productos' debe ser una lista de tuplas: [(id_producto, cantidad), ...]
        """
        conexion = self.obtener_conexion()
        if not conexion: return False

        try:
            # 1. Desactivamos el autocommit para manejar la transacción manualmente
            conexion.autocommit = False
            cursor = conexion.cursor(dictionary=True)

            # 2. Calcular el total acumulado y validar stock antes de hacer nada
            total_pedido = 0.0
            detalles_a_insertar = []

            for id_prod, cant in lista_productos:
                # Buscar precio y stock actual del producto
                cursor.execute("SELECT precio, stock_actual, nombre FROM productos WHERE id_producto = %s", (id_prod,))
                producto = cursor.fetchone()

                if not producto:
                    print(f"\n❌ El producto con ID {id_prod} no existe.")
                    conexion.rollback()
                    return False
                
                if producto['stock_actual'] < cant:
                    print(f"\n❌ Stock insuficiente para '{producto['nombre']}'. Disponible: {producto['stock_actual']}")
                    conexion.rollback()
                    return False

                subtotal = float(producto['precio']) * cant
                total_pedido += subtotal
                detalles_a_insertar.append((id_prod, cant, producto['precio']))

            # 3. Crear la cabecera del Pedido
            query_pedido = "INSERT INTO pedidos (id_cliente, total, estado) VALUES (%s, %s, 'Pagado')"
            cursor.execute(query_pedido, (id_cliente, total_pedido))
            id_nuevo_pedido = cursor.lastrowid # Obtenemos el ID generado para el pedido

            # 4. Insertar los detalles y restar stock
            query_detalle = """INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario) 
                               VALUES (%s, %s, %s, %s)"""
            query_stock = "UPDATE productos SET stock_actual = stock_actual - %s WHERE id_producto = %s"

            for id_prod, cant, precio in detalles_a_insertar:
                # Insertar en detalle
                cursor.execute(query_detalle, (id_nuevo_pedido, id_prod, cant, precio))
                # Descontar stock
                cursor.execute(query_stock, (cant, id_prod))

            # 5. Si todo salió bien, confirmamos los cambios en la base de datos
            conexion.commit()
            print(f"\n✅ ¡Pedido #{id_nuevo_pedido} registrado con éxito! Total: ${total_pedido:.2f}")
            cursor.close()
            return True

        except Error as e:
            # Si hubo cualquier error, deshacemos todo para no dejar datos corruptos
            conexion.rollback()
            print(f"❌ Error en la transacción del pedido: {e}")
            return False
        finally:
            conexion.close()