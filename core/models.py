from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

@dataclass
class Producto:
    """Modelo de producto de librería"""
    id: Optional[int] = None
    codigo: str = ""  # ej: "345-0019"
    descripcion: str = ""  # ej: "ABACO MARTIZ Nº7/10"
    precio_unitario: Decimal = Decimal("0.00")  # ej: 8434.80
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row["id"],
            codigo=row["codigo"],
            descripcion=row["descripcion"],
            precio_unitario=Decimal(str(row["precio_unitario"]))
        )
    
    def get_precio_formateado(self) -> str:
        """Retorna el precio en formato argentino: $ 8.434,80"""
        return f"$ {self.precio_unitario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
@dataclass
class DetalleCompra:
    """Una línea de la compra"""
    id: Optional[int] = None
    compra_id: Optional[int] = None
    codigo_producto: str = ""
    descripcion: str = ""
    precio_unitario: Decimal = Decimal("0.00")
    cantidad: int = 0
    subtotal: Decimal = Decimal("0.00")
    
    def calcular_subtotal(self):
        self.subtotal = self.precio_unitario * self.cantidad
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row["id"],
            compra_id=row["compra_id"],
            codigo_producto=row["codigo_producto"],
            descripcion=row["descripcion"],
            precio_unitario=Decimal(str(row["precio_unitario"])),
            cantidad=row["cantidad"],
            subtotal=Decimal(str(row["subtotal"]))
        )


@dataclass
class Compra:
    """Cabecera de la compra"""
    id: Optional[int] = None
    fecha: Optional[str] = None  # Cambiado a str para manejar "YYYY-MM-DD"
    cantidad_items: int = 0
    total: Decimal = Decimal("0.00")
    # Lista de detalles (no se guarda en DB directamente)
    detalles: List[DetalleCompra] = field(default_factory=list, repr=False)
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row["id"],
            fecha=row["fecha"],  # Ya viene como string desde SQLite
            cantidad_items=row["cantidad_items"],
            total=Decimal(str(row["total"]))
        )
    
    def get_fecha_formateada(self) -> str:
        """Formatea la fecha para mostrar: 27/06/2026"""
        if not self.fecha:
            return ""
        # Si viene como "2026-06-27 10:30:00", tomamos solo la fecha
        if " " in self.fecha:
            self.fecha = self.fecha.split(" ")[0]
        # Convertir de "YYYY-MM-DD" a "DD/MM/YYYY"
        try:
            partes = self.fecha.split("-")
            if len(partes) == 3:
                return f"{partes[2]}/{partes[1]}/{partes[0]}"
        except:
            pass
        return self.fecha
    
    def get_total_formateado(self) -> str:
        return f"$ {self.total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")    