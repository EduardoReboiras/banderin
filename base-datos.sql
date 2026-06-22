
CREATE DATABASE IF NOT EXISTS libreria_banderin;
USE libreria_banderin;


CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empresa VARCHAR(100) NOT NULL,
    contacto_nombre VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- 3. Tabla de Productos (El corazón del inventario)
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5, -- Alerta cuando quede poco
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

-- 4. Tabla de Clientes / Usuarios
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Para guardar la clave segura
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de Pedidos (La cabecera de la compra)
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Pendiente', -- Pendiente, Pagado, Enviado, Cancelado
    total DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- 6. Detalle de Pedidos (Relación Muchos a Muchos entre Pedidos y Productos)
CREATE TABLE detalle_pedidos (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL, -- Guardamos el precio del momento
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

INSERT INTO proveedores (nombre_empresa, contacto_nombre, telefono, email) 
VALUES 
('Distribuidora Sur', 'Juan Pérez', '1122334455', 'contacto@sur.com'),
('TecnoMayorista', 'Ana Gómez', '1166778899', 'ventas@tecnomayorista.com'),
('Bazar Central', 'Carlos López', '1155443322', 'carlos@bazarcentral.com');

INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, id_proveedor) 
VALUES 
('Teclado Mecánico RGB', 'Teclado con switches red, ideal para gaming', 45000.00, 15, 3, 2),
('Mouse Óptico Inalámbrico', 'Mouse ergonómico 2400 DPI', 18000.00, 25, 5, 2),
('Monitor 24" FullHD', 'Monitor tasa de refresco 75Hz panel IPS', 140000.00, 8, 2, 2),
('Auriculares con Micrófono', 'Conexión Jack 3.5mm y USB para luces', 28000.00, 0, 4, 1),
('Silla Escritorio Ergonómica', 'Silla con soporte lumbar regulable', 95000.00, 4, 2, 3);