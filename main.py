from database import LibreriaBD
import sys

def menu_principal():
    db = LibreriaBD()

    while True:
        print("\n" + "="*40)
        print("     SISTEMA LIBRERÍA BANDERÍN")
        print("="*40)
        print("1. Buscar Producto")
        print("2. Ver Alertas de Stock Mínimo")
        print("3. Registrar Nuevo Cliente")
        print("4. Simular Venta/Pedido") # <-- Nueva opción
        print("5. Salir")
        print("="*40)
        
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == "1":
            nombre = input("\nIngresa el nombre del producto a buscar: ")
            productos = db.buscar_producto_por_nombre(nombre)
            if productos:
                print(f"\nResultados para '{nombre}':")
                for p in productos:
                    print(f"- ID: {p['id_producto']} | {p['nombre']} | Precio: ${p['precio']} | Stock: {p['stock_actual']}")
            else:
                print("\nNo se encontraron productos.")

        elif opcion == "2":
            alertas = db.verificar_stock_critico()
            if alertas:
                print("\n⚠️ ¡ALERTAS DE STOCK CRÍTICO! Reponer cuanto antes:")
                for a in alertas:
                    print(f"- {a['nombre']}: Stock actual {a['stock_actual']} (Mínimo requerido: {a['stock_minimo']})")
            else:
                print("\n✅ Todo en orden. Todos los productos tienen stock suficiente.")

        elif opcion == "3":
            print("\n--- Registro de Cliente ---")
            nom = input("Nombre: ")
            ape = input("Apellido: ")
            email = input("Email: ")
            passw = input("Contraseña: ")
            
            if db.registrar_cliente(nom, ape, email, passw):
                print(f"\n¡Cliente {nom} {ape} registrado con éxito!")
            else:
                print("\nNo se pudo registrar al cliente. Verifica si el email ya existe.")

        elif opcion == "4":
            print("\n--- Simular Nueva Venta ---")
            # Para la simulación usamos el cliente ID 1 (puedes verificar en tu tabla de clientes)
            try:
                id_cliente = int(input("ID del Cliente que compra (ej: 1): "))
                
                carrito = []
                while True:
                    id_prod = input("ID del Producto (o 'fin' para terminar): ")
                    if id_prod.lower() == 'fin':
                        break
                    cant = int(input(f"Cantidad para el producto {id_prod}: "))
                    carrito.append((int(id_prod), cant))

                if carrito:
                    db.realizar_pedido(id_cliente, carrito)
                else:
                    print("\nCarrito vacío. Proceso cancelado.")
            except ValueError:
                print("\n❌ Error: Ingresa números válidos para los IDs y cantidades.")

        elif opcion == "5":
            print("\n¡Gracias por usar el sistema! Saliendo...")
            sys.exit()
        else:
            print("\nOpción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()