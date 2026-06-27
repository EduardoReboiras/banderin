from core.database import Database
from core.models import Compra, DetalleCompra
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class CompraService:
    def __init__(self):
        self.db = Database()
    
    def crear_compra(self, detalles: List[DetalleCompra], fecha: str) -> Optional[int]:
        """
        Crea una compra completa con todos sus detalles.
        :param fecha: Fecha en formato "YYYY-MM-DD" (ej: "2026-06-27")
        """
        if not detalles:
            return None
        
        try:
            cantidad_items = len(detalles)
            total = sum(d.subtotal for d in detalles)
            
            cursor = self.db.execute("""
                INSERT INTO compras (fecha, cantidad_items, total)
                VALUES (?, ?, ?)
            """, (fecha, cantidad_items, float(total)))
            compra_id = cursor.lastrowid
            
            for detalle in detalles:
                self.db.execute("""
                    INSERT INTO detalle_compras 
                    (compra_id, codigo_producto, descripcion, precio_unitario, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    compra_id,
                    detalle.codigo_producto,
                    detalle.descripcion,
                    float(detalle.precio_unitario),
                    detalle.cantidad,
                    float(detalle.subtotal)
                ))
            
            return compra_id
        except Exception as e:
            print(f"Error al crear compra: {e}")
            return None
    
    def obtener_historial(self) -> List[Compra]:
        """Obtiene todas las compras ordenadas por fecha descendente"""
        rows = self.db.fetch_all("""
            SELECT * FROM compras 
            ORDER BY fecha DESC
        """)
        return [Compra.from_row(r) for r in rows]
    
    def obtener_compra_completa(self, compra_id: int) -> Optional[Compra]:
        """Obtiene una compra con todos sus detalles"""
        # Cabecera
        row = self.db.fetch_one(
            "SELECT * FROM compras WHERE id=?", (compra_id,)
        )
        if not row:
            return None
        
        compra = Compra.from_row(row)
        
        # Detalles
        detalles_rows = self.db.fetch_all("""
            SELECT * FROM detalle_compras 
            WHERE compra_id=? 
            ORDER BY id
        """, (compra_id,))
        compra.detalles = [DetalleCompra.from_row(r) for r in detalles_rows]
        
        return compra
    
    def eliminar_compra(self, compra_id: int) -> bool:
        """Elimina una compra y sus detalles (cascade)"""
        try:
            self.db.execute("DELETE FROM compras WHERE id=?", (compra_id,))
            return True
        except Exception:
            return False