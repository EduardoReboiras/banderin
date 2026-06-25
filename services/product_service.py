# services/product_service.py
from core.database import Database
from core.models import Producto
from typing import List, Optional
from decimal import Decimal


class ProductService:
    def __init__(self):
        self.db = Database()
    
    def crear(self, producto: Producto) -> Optional[int]:
        """Crea un nuevo producto. Retorna el ID o None si hay error."""
        try:
            cursor = self.db.execute("""
                INSERT INTO productos (codigo, descripcion, precio_unitario)
                VALUES (?, ?, ?)
            """, (producto.codigo, producto.descripcion, float(producto.precio_unitario)))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Código duplicado
            return None
    
    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos ordenados por descripción"""
        rows = self.db.fetch_all(
            "SELECT * FROM productos ORDER BY descripcion"
        )
        return [Producto.from_row(r) for r in rows]
    
    def buscar_por_codigo(self, texto: str) -> List[Producto]:
        """Busca productos por código (búsqueda parcial)"""
        pattern = f"%{texto}%"
        rows = self.db.fetch_all("""
            SELECT * FROM productos 
            WHERE codigo LIKE ?
            ORDER BY codigo
        """, (pattern,))
        return [Producto.from_row(r) for r in rows]
    
    def buscar_por_descripcion(self, texto: str) -> List[Producto]:
        """Busca productos por descripción (búsqueda parcial)"""
        pattern = f"%{texto}%"
        rows = self.db.fetch_all("""
            SELECT * FROM productos 
            WHERE descripcion LIKE ?
            ORDER BY descripcion
        """, (pattern,))
        return [Producto.from_row(r) for r in rows]
    
    def buscar(self, texto: str) -> List[Producto]:
        """Búsqueda combinada: código O descripción"""
        pattern = f"%{texto}%"
        rows = self.db.fetch_all("""
            SELECT * FROM productos 
            WHERE codigo LIKE ? OR descripcion LIKE ?
            ORDER BY descripcion
        """, (pattern, pattern))
        return [Producto.from_row(r) for r in rows]
    
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        row = self.db.fetch_one(
            "SELECT * FROM productos WHERE id=?", (id,)
        )
        return Producto.from_row(row)
    
    def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por su código exacto"""
        row = self.db.fetch_one(
            "SELECT * FROM productos WHERE codigo=?", (codigo,)
        )
        return Producto.from_row(row)
    
    def actualizar(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        try:
            self.db.execute("""
                UPDATE productos 
                SET codigo=?, descripcion=?, precio_unitario=?
                WHERE id=?
            """, (producto.codigo, producto.descripcion, 
                  float(producto.precio_unitario), producto.id))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un producto por su ID"""
        try:
            self.db.execute(
                "DELETE FROM productos WHERE id=?", (id,)
            )
            return True
        except Exception:
            return False