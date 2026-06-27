
from PySide6.QtCore import QAbstractTableModel, Qt
from core.models import Compra


class CompraTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Fecha", "Cantidad Items", "Total"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._compras: list[Compra] = []
    
    def set_compras(self, compras: list[Compra]):
        self.beginResetModel()
        self._compras = compras
        self.endResetModel()
    
    def get_compra(self, row: int) -> Compra:
        return self._compras[row]
    
    def rowCount(self, parent=None):
        return len(self._compras)
    
    def columnCount(self, parent=None):
        return len(self.HEADERS)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        compra = self._compras[index.row()]
        col = index.column()
        
        if role == Qt.DisplayRole:
            valores = [
                compra.id,
                compra.get_fecha_formateada(),
                compra.cantidad_items,
                compra.get_total_formateado()
            ]
            return valores[col]
        
        if role == Qt.TextAlignmentRole:
            if col in (0, 2):  # ID y Cantidad centrados
                return Qt.AlignCenter
            elif col == 3:  # Total a la derecha
                return Qt.AlignRight | Qt.AlignVCenter
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return None