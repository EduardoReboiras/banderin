from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


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