# ui/widgets/product_table_model.py
from PySide6.QtCore import QAbstractTableModel, Qt
from core.models import Producto


class ProductTableModel(QAbstractTableModel):
    """Modelo de tabla para productos"""
    HEADERS = ["Código", "Descripción", "Precio Unitario"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._productos: list[Producto] = []
    
    def set_productos(self, productos: list[Producto]):
        """Actualiza la lista de productos"""
        self.beginResetModel()
        self._productos = productos
        self.endResetModel()
    
    def get_producto(self, row: int) -> Producto:
        """Obtiene el producto de una fila"""
        return self._productos[row]
    
    def rowCount(self, parent=None):
        return len(self._productos)
    
    def columnCount(self, parent=None):
        return len(self.HEADERS)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        producto = self._productos[index.row()]
        col = index.column()
        
        if role == Qt.DisplayRole:
            valores = [
                producto.codigo,
                producto.descripcion,
                producto.get_precio_formateado()
            ]
            return valores[col]
        
        if role == Qt.TextAlignmentRole:
            if col == 0:  # Código: centrado
                return Qt.AlignCenter
            elif col == 2:  # Precio: alineado a la derecha
                return Qt.AlignRight | Qt.AlignVCenter
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return None